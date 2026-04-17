"""
DES Encryption/Decryption utilities for UA Parking System
Uses 3DES (Triple DES) for enhanced security
"""

from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import json

# Encryption key (32 bytes for 3DES with 3 keys = 192 bits)
# In production, this should be stored in environment variables
ENCRYPTION_KEY = b'UA_PARKING_SYSTEM_SECRET_KEY_2026'[:24]  # 24 bytes for 3DES


class DESEncryption:
    """DES/3DES encryption and decryption utilities"""

    @staticmethod
    def encrypt(data):
        """
        Encrypt data using 3DES in CBC mode
        
        Args:
            data (str): Plain text data to encrypt
            
        Returns:
            str: Base64 encoded encrypted data
        """
        try:
            # Generate random IV (Initialization Vector)
            iv = get_random_bytes(8)
            
            # Create cipher
            cipher = DES3.new(ENCRYPTION_KEY, DES3.MODE_CBC, iv)
            
            # Pad data to multiple of 8 bytes (DES block size)
            padded_data = pad(data.encode('utf-8'), DES3.block_size)
            
            # Encrypt
            encrypted_data = cipher.encrypt(padded_data)
            
            # Combine IV + encrypted data and encode to base64
            combined = iv + encrypted_data
            encoded = base64.b64encode(combined).decode('utf-8')
            
            return encoded
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")

    @staticmethod
    def decrypt(encrypted_data):
        """
        Decrypt data using 3DES in CBC mode
        
        Args:
            encrypted_data (str): Base64 encoded encrypted data
            
        Returns:
            str: Decrypted plain text data
        """
        try:
            # Decode from base64
            combined = base64.b64decode(encrypted_data)
            
            # Extract IV and encrypted data
            iv = combined[:8]
            actual_encrypted_data = combined[8:]
            
            # Create cipher
            cipher = DES3.new(ENCRYPTION_KEY, DES3.MODE_CBC, iv)
            
            # Decrypt
            padded_data = cipher.decrypt(actual_encrypted_data)
            
            # Unpad
            data = unpad(padded_data, DES3.block_size)
            
            return data.decode('utf-8')
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")

    @staticmethod
    def encrypt_dict(data_dict):
        """
        Encrypt a dictionary to JSON string then encrypt
        
        Args:
            data_dict (dict): Dictionary to encrypt
            
        Returns:
            str: Base64 encoded encrypted JSON
        """
        json_str = json.dumps(data_dict)
        return DESEncryption.encrypt(json_str)

    @staticmethod
    def decrypt_dict(encrypted_data):
        """
        Decrypt data to JSON string then parse to dictionary
        
        Args:
            encrypted_data (str): Base64 encoded encrypted JSON
            
        Returns:
            dict: Decrypted dictionary
        """
        json_str = DESEncryption.decrypt(encrypted_data)
        return json.loads(json_str)
