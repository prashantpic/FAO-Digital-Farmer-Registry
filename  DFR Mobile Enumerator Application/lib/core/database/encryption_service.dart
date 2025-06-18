```dart
import 'dart:convert';
import 'dart:math';
import 'package:dfr_mobile/core/security/secure_storage_service.dart';
import 'package:dfr_mobile/injection_container.dart'; // For getIt

/// Service responsible for managing the database encryption key.
///
/// It securely retrieves an existing key or generates and stores a new one
/// using [SecureStorageService]. This key is then used by [DatabaseHelper]
/// for SQLCipher encryption.
class EncryptionService {
  final SecureStorageService _secureStorageService;

  // REQ-CONF-002: Alias for storing the DB encryption key
  static const String _dbEncryptionKeyAlias = 'dfr_db_encryption_key';

  EncryptionService({SecureStorageService? secureStorageService})
      : _secureStorageService = secureStorageService ?? getIt<SecureStorageService>();

  /// Retrieves the database encryption key.
  ///
  /// Tries to read the key from secure storage. If the key doesn't exist,
  /// it generates a new strong random key (32 bytes, Base64 URL encoded),
  /// stores it securely, and then returns it.
  Future<String> getDatabaseEncryptionKey() async {
    String? key = await _secureStorageService.read(key: _dbEncryptionKeyAlias);

    if (key == null || key.isEmpty) {
      // Generate a new strong random key (256-bit / 32 bytes)
      final random = Random.secure();
      final keyBytes = List<int>.generate(32, (_) => random.nextInt(256));
      // Using base64UrlEncode for compatibility with various systems,
      // though SQLCipher PRAGMA key typically expects hex or raw string.
      // For PRAGMA key = 'somekey', 'somekey' is used directly.
      // For PRAGMA key = "x'hexkey'", hexkey is used.
      // A simple strong string is often sufficient. Base64 is fine.
      // SQLCipher itself will use this string as a passphrase for key derivation.
      final newKey = base64UrlEncode(keyBytes); 
      
      await _secureStorageService.write(key: _dbEncryptionKeyAlias, value: newKey);
      return newKey;
    }
    return key;
  }

  /// !!! DANGER ZONE !!!
  /// Clears the stored database encryption key.
  /// This is typically only used for development, testing, or a full reset.
  /// Calling this without proper data backup WILL lead to data loss
  /// as the encrypted database will become inaccessible.
  Future<void> clearDatabaseEncryptionKeyForDevelopment() async {
    // Add checks here, e.g., only allow in debug mode.
    // if (kReleaseMode) {
    //   throw Exception("Cannot clear encryption key in release mode.");
    // }
    await _secureStorageService.delete(key: _dbEncryptionKeyAlias);
  }
}
```