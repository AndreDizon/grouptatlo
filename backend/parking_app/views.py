from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta, date, datetime

from .models import (
    Vehicle, ParkingPass, ParkingSession,
    ParkingLot, ParkingRate, Announcement, ScanLog
)
from .serializers import (
    VehicleSerializer, ParkingPassSerializer,
    ParkingSessionSerializer, ParkingLotSerializer, ParkingRateSerializer,
    AnnouncementSerializer, ScanLogSerializer, UserSerializer
)


# ============ Authentication Endpoint ============
@api_view(['POST'])
def login_view(request):
    """
    Login endpoint to authenticate users.
    Expected POST data: { "username": "...", "password": "..." }
    Returns: { "id": ..., "username": "...", "email": "...", "role": "...", "first_name": "...", "last_name": "..." }
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Authenticate against Django user database
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Determine role: admin if superuser, guard if staff, else driver
        if user.is_superuser:
            role = 'admin'
        elif user.is_staff:
            role = 'guard'
        else:
            role = 'driver'
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': role,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
def register_view(request):
    """
    Registration endpoint to create new driver users.
    Expected POST data: { "username": "...", "password": "..." }
    Returns: { "id": ..., "username": "...", "role": "driver" }
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already taken'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create new user with driver role (is_staff=False, is_superuser=False)
    try:
        user = User.objects.create_user(
            username=username,
            password=password,
            is_staff=False,
            is_superuser=False
        )
        
        return Response({
            'id': user.id,
            'username': user.username,
            'role': 'driver',
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """User viewset with filtering support"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['username', 'email']
    search_fields = ['username', 'email', 'first_name', 'last_name']

    def get_queryset(self):
        # If user is authenticated and staff, return all users
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return User.objects.all()
        # If user is authenticated but not staff, return only their own user
        if self.request.user.is_authenticated:
            return User.objects.filter(id=self.request.user.id)
        # If user is not authenticated, return all users (since permission_classes = [AllowAny])
        return User.objects.all()

    def perform_create(self, serializer):
        """Create user and set flags based on role"""
        # Get the role from request data
        role = self.request.data.get('role', 'driver')
        
        # Save the user
        user = serializer.save()
        
        # Set staff/superuser status based on role
        if role == 'admin':
            user.is_staff = True
            user.is_superuser = True
        elif role == 'guard':
            user.is_staff = True
            user.is_superuser = False
        else:
            # driver
            user.is_staff = False
            user.is_superuser = False
        
        user.save()


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['owner', 'plate_number', 'vehicle_type']
    search_fields = ['plate_number', 'brand', 'model']
    ordering_fields = ['registration_date']
    ordering = ['-registration_date']

    def get_queryset(self):
        queryset = Vehicle.objects.all()
        
        # Filter by owner_id query parameter if provided (for unauthenticated frontend requests)
        owner_id = self.request.query_params.get('owner')
        if owner_id:
            try:
                owner_id = int(owner_id)  # Convert to integer
                queryset = queryset.filter(owner_id=owner_id)
            except (ValueError, TypeError):
                # If owner_id is not a valid integer, just return all vehicles
                pass
        # If user is authenticated, return only their own vehicles (unless they're staff)
        elif self.request.user.is_authenticated and not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        
        return queryset

    def perform_create(self, serializer):
        # If owner is already in the data, use it
        if 'owner' in serializer.validated_data:
            vehicle = serializer.save(is_registered=True)
        else:
            # Otherwise, set owner to the authenticated user
            vehicle = serializer.save(owner=self.request.user, is_registered=True)
        
        # Auto-generate QR code after vehicle is created
        vehicle.generate_qr_code()
        vehicle.save()

    @action(detail=True, methods=['post'])
    def mark_registered(self, request, pk=None):
        """Mark vehicle as registered"""
        vehicle = self.get_object()
        vehicle.is_registered = True
        vehicle.save()
        return Response({'message': 'Vehicle marked as registered', 'is_registered': vehicle.is_registered})

    @action(detail=True, methods=['post'])
    def mark_unregistered(self, request, pk=None):
        """Mark vehicle as unregistered"""
        vehicle = self.get_object()
        vehicle.is_registered = False
        vehicle.save()
        return Response({'message': 'Vehicle marked as unregistered', 'is_registered': vehicle.is_registered})

    @action(detail=True, methods=['post'])
    def mark_paid(self, request, pk=None):
        """Mark vehicle as paid"""
        vehicle = self.get_object()
        vehicle.is_paid = True
        vehicle.save()
        return Response({'message': 'Vehicle marked as paid', 'is_paid': vehicle.is_paid})

    @action(detail=True, methods=['post'])
    def mark_unpaid(self, request, pk=None):
        """Mark vehicle as unpaid"""
        vehicle = self.get_object()
        vehicle.is_paid = False
        vehicle.save()
        return Response({'message': 'Vehicle marked as unpaid', 'is_paid': vehicle.is_paid})

    @action(detail=True, methods=['post'])
    def generate_qr(self, request, pk=None):
        vehicle = self.get_object()
        vehicle.generate_qr_code()
        vehicle.save()
        return Response({'message': 'QR code generated successfully'})


class ParkingRateViewSet(viewsets.ModelViewSet):
    queryset = ParkingRate.objects.all()
    serializer_class = ParkingRateSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Handle creation - prevent duplicate vehicle_type + pass_type combinations"""
        vehicle_type = request.data.get('vehicle_type')
        pass_type = request.data.get('pass_type')
        
        # Check if rate with same vehicle_type and pass_type already exists
        existing_rate = ParkingRate.objects.filter(
            vehicle_type=vehicle_type,
            pass_type=pass_type
        ).first()
        
        if existing_rate:
            # Return clear error that this combination already exists
            return Response({
                'error': f'A pricing tier for {vehicle_type} + {pass_type} already exists. Use the Edit button to modify it.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create new rate only if combination doesn't exist
        return super().create(request, *args, **kwargs)


class ParkingPassViewSet(viewsets.ModelViewSet):
    serializer_class = ParkingPassSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # If user is authenticated and staff, return all passes
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return ParkingPass.objects.all()
        # If user is authenticated but not staff, return only their passes
        if self.request.user.is_authenticated:
            return ParkingPass.objects.filter(vehicle__owner=self.request.user)
        # If user is not authenticated, return all passes (since permission_classes = [AllowAny])
        return ParkingPass.objects.all()


class ParkingSessionViewSet(viewsets.ModelViewSet):
    serializer_class = ParkingSessionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['vehicle', 'scanned_by', 'parking_lot']
    search_fields = ['vehicle__plate_number']
    ordering_fields = ['time_in', 'time_out']
    ordering = ['-time_in']

    def get_queryset(self):
        # If user is authenticated and staff, return all sessions
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return ParkingSession.objects.all()
        # If user is authenticated but not staff, return only their sessions
        if self.request.user.is_authenticated:
            return ParkingSession.objects.filter(vehicle__owner=self.request.user)
        # If user is not authenticated, return all sessions (since permission_classes = [AllowAny])
        return ParkingSession.objects.all()

    @action(detail=False, methods=['post'])
    def check_in(self, request):
        vehicle_id = request.data.get('vehicle_id')
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id, owner=request.user)
            session = ParkingSession.objects.create(
                vehicle=vehicle,
                time_in=timezone.now(),
                scanned_by=request.user if request.user.is_staff else None
            )
            return Response(ParkingSessionSerializer(session).data, status=status.HTTP_201_CREATED)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        session = self.get_object()
        session.time_out = timezone.now()
        session.save()
        return Response(ParkingSessionSerializer(session).data)

    @action(detail=False, methods=['get'])
    def active_sessions(self, request):
        sessions = ParkingSession.objects.filter(time_out__isnull=True)
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today_sessions(self, request):
        """Get today's parking sessions for the current user"""
        user_id = request.query_params.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user_id = int(user_id)
            # Get all vehicles for the user
            user_vehicles = Vehicle.objects.filter(owner_id=user_id)
            user_vehicle_ids = user_vehicles.values_list('id', flat=True)
            
            # Get today's date range
            today = date.today()
            today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
            today_end = timezone.make_aware(datetime.combine(today, datetime.max.time()))
            
            # Filter sessions for user's vehicles that occurred today
            sessions = ParkingSession.objects.filter(
                vehicle_id__in=user_vehicle_ids,
                time_in__gte=today_start,
                time_in__lt=today_end
            ).order_by('-time_in')
            
            serializer = self.get_serializer(sessions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid user_id'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ParkingLotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ParkingLot.objects.filter(is_active=True)
    serializer_class = ParkingLotSerializer
    permission_classes = [AllowAny]


class AnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Announcement.objects.filter(is_active=True)
    serializer_class = AnnouncementSerializer
    permission_classes = [AllowAny]


class ScanLogViewSet(viewsets.ModelViewSet):
    serializer_class = ScanLogSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # If user is authenticated and staff, return all scan logs
        if self.request.user.is_authenticated and self.request.user.is_staff:
            return ScanLog.objects.all()
        # If user is authenticated but not staff, return only their scan logs
        if self.request.user.is_authenticated:
            return ScanLog.objects.filter(guard=self.request.user)
        # If user is not authenticated, return all scan logs (since permission_classes = [AllowAny])
        return ScanLog.objects.all()

    @action(detail=False, methods=['post'])
    def scan_qr(self, request):
        qr_data = request.data.get('qr_data')
        scan_type = request.data.get('scan_type', 'in')
        guard_id = request.data.get('guard_id')  # Get guard ID from frontend
        
        try:
            vehicle_id = qr_data.split('_')[2]
            vehicle = Vehicle.objects.get(id=vehicle_id)
            
            # Determine guard: use guard_id from request if provided, otherwise use authenticated user
            guard = None
            if guard_id:
                try:
                    guard = User.objects.get(id=guard_id)
                except User.DoesNotExist:
                    guard = request.user if request.user.is_authenticated else None
            else:
                guard = request.user if request.user.is_authenticated else None
            
            # Create scan log with guard information
            scan_log = ScanLog.objects.create(
                guard=guard,
                vehicle=vehicle,
                scan_type=scan_type,
                manual_entry=False
            )
            
            if scan_type == 'in':
                ParkingSession.objects.create(
                    vehicle=vehicle,
                    time_in=timezone.now(),
                    scanned_by=guard
                )
            else:
                session = ParkingSession.objects.filter(
                    vehicle=vehicle,
                    time_out__isnull=True
                ).first()
                if session:
                    session.time_out = timezone.now()
                    session.scanned_by = guard  # Record which guard did the time-out
                    session.save()
            
            return Response(ScanLogSerializer(scan_log).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def manual_entry(self, request):
        plate_number = request.data.get('plate_number').upper()
        scan_type = request.data.get('scan_type', 'in')
        guard_id = request.data.get('guard_id')  # Get guard ID from frontend
        
        try:
            vehicle = Vehicle.objects.get(plate_number=plate_number)
            
            # Determine guard: use guard_id from request if provided, otherwise use authenticated user
            guard = None
            if guard_id:
                try:
                    guard = User.objects.get(id=guard_id)
                except User.DoesNotExist:
                    guard = request.user if request.user.is_authenticated else None
            else:
                guard = request.user if request.user.is_authenticated else None
            
            scan_log = ScanLog.objects.create(
                guard=guard,
                vehicle=vehicle,
                scan_type=scan_type,
                manual_entry=True,
                notes=request.data.get('notes', '')
            )
            
            if scan_type == 'in':
                ParkingSession.objects.create(
                    vehicle=vehicle,
                    time_in=timezone.now(),
                    scanned_by=guard
                )
            else:
                session = ParkingSession.objects.filter(
                    vehicle=vehicle,
                    time_out__isnull=True
                ).first()
                if session:
                    session.time_out = timezone.now()
                    session.scanned_by = guard  # Record which guard did the time-out
                    session.save()
            
            return Response(ScanLogSerializer(scan_log).data, status=status.HTTP_201_CREATED)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def guard_statistics(self, request):
        """Get scan statistics for a specific guard by date range"""
        guard_id = request.query_params.get('guard_id')
        filter_type = request.query_params.get('filter', 'day')  # day, week, month, year
        
        if not guard_id:
            return Response(
                {'error': 'guard_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            guard_id = int(guard_id)
            
            # Calculate date range
            today = date.today()
            if filter_type == 'day':
                start_date = timezone.make_aware(datetime.combine(today, datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(today, datetime.max.time()))
            elif filter_type == 'week':
                # Get 7 days back
                start_date = timezone.make_aware(datetime.combine(today - timedelta(days=7), datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(today, datetime.max.time()))
            elif filter_type == 'month':
                # Get all from this month
                start_date = timezone.make_aware(datetime.combine(today.replace(day=1), datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(today, datetime.max.time()))
            elif filter_type == 'year':
                # Get all from this year
                start_date = timezone.make_aware(datetime.combine(today.replace(month=1, day=1), datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(today, datetime.max.time()))
            else:
                start_date = timezone.make_aware(datetime.combine(today, datetime.min.time()))
                end_date = timezone.make_aware(datetime.combine(today, datetime.max.time()))
            
            # Filter scan logs by guard and date range
            scan_logs = ScanLog.objects.filter(
                guard_id=guard_id,
                scan_time__gte=start_date,
                scan_time__lte=end_date
            )
            
            # Calculate statistics
            total_scanned = scan_logs.values('vehicle_id').distinct().count()
            time_ins = scan_logs.filter(scan_type='in').count()
            time_outs = scan_logs.filter(scan_type='out').count()
            manual_entries = scan_logs.filter(manual_entry=True).count()
            
            return Response({
                'total_scanned': total_scanned,
                'time_ins': time_ins,
                'time_outs': time_outs,
                'manual_entries': manual_entries,
                'date_range': {
                    'start': start_date.isoformat(),
                    'end': end_date.isoformat(),
                    'filter': filter_type
                }
            }, status=status.HTTP_200_OK)
        except (ValueError, TypeError):
            return Response(
                {'error': 'Invalid guard_id'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def debug_all_scans(self, request):
        """Debug endpoint: Return all scan logs for troubleshooting"""
        try:
            all_scans = ScanLog.objects.all().order_by('-scan_time')
            data = []
            for scan in all_scans:
                data.append({
                    'id': scan.id,
                    'guard_id': scan.guard_id,
                    'guard_name': scan.guard.get_full_name() if scan.guard else 'None',
                    'vehicle_id': scan.vehicle_id,
                    'vehicle_plate': scan.vehicle.plate_number if scan.vehicle else 'None',
                    'scan_type': scan.scan_type,
                    'scan_time': scan.scan_time.isoformat(),
                    'manual_entry': scan.manual_entry
                })
            return Response({
                'total_scans': len(data),
                'scans': data
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
