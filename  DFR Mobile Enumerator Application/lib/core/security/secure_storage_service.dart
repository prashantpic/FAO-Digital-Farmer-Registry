import 'package:flutter_secure_storage/flutter_secure_storage.dart';

/// A service class for securely storing sensitive data.
///
/// This class acts as a wrapper around `flutter_secure_storage`,
/// utilizing platform-provided mechanisms like Android Keystore or iOS Keychain
/// to store data such as encryption keys, API tokens, etc.
class SecureStorageService {
  final FlutterSecureStorage _storage;

  /// Creates an instance of [SecureStorageService].
  ///
  /// Optionally, a [FlutterSecureStorage] instance can be provided for testing,
  /// otherwise a default instance is created.
  SecureStorageService({FlutterSecureStorage? storage})
      : _storage = storage ?? const FlutterSecureStorage();

  /// Returns Android specific options for `flutter_secure_storage`.
  ///
  /// Enables `encryptedSharedPreferences` to ensure data is stored
  /// in encrypted shared preferences, backed by Android Keystore where available.
  AndroidOptions _getAndroidOptions() => const AndroidOptions(
        encryptedSharedPreferences: true,
      );

  /// Writes a value to secure storage.
  ///
  /// - [key]: The key under which to store the value.
  /// - [value]: The value to store.
  ///
  /// Throws a [PlatformException] if an error occurs during writing.
  Future<void> write({required String key, required String value}) async {
    try {
      await _storage.write(
        key: key,
        value: value,
        aOptions: _getAndroidOptions(),
        // iOptions: _getIOSOptions(), // Add iOS options if needed
      );
    } catch (e) {
      // TODO: Log error using a LoggingService
      print('Error writing to secure storage: $e');
      rethrow;
    }
  }

  /// Reads a value from secure storage.
  ///
  /// - [key]: The key of the value to read.
  ///
  /// Returns the stored value, or `null` if the key is not found.
  /// Throws a [PlatformException] if an error occurs during reading.
  Future<String?> read({required String key}) async {
    try {
      return await _storage.read(
        key: key,
        aOptions: _getAndroidOptions(),
        // iOptions: _getIOSOptions(), // Add iOS options if needed
      );
    } catch (e) {
      // TODO: Log error using a LoggingService
      print('Error reading from secure storage: $e');
      rethrow;
    }
  }

  /// Deletes a value from secure storage.
  ///
  /// - [key]: The key of the value to delete.
  ///
  /// Throws a [PlatformException] if an error occurs during deletion.
  Future<void> delete({required String key}) async {
    try {
      await _storage.delete(
        key: key,
        aOptions: _getAndroidOptions(),
        // iOptions: _getIOSOptions(), // Add iOS options if needed
      );
    } catch (e) {
      // TODO: Log error using a LoggingService
      print('Error deleting from secure storage: $e');
      rethrow;
    }
  }

  /// Deletes all values from secure storage.
  ///
  /// **Warning:** This will remove all data stored by the app via this plugin.
  /// Use with caution.
  ///
  /// Throws a [PlatformException] if an error occurs during deletion.
  Future<void> deleteAll() async {
    try {
      await _storage.deleteAll(
        aOptions: _getAndroidOptions(),
        // iOptions: _getIOSOptions(), // Add iOS options if needed
      );
    } catch (e) {
      // TODO: Log error using a LoggingService
      print('Error deleting all from secure storage: $e');
      rethrow;
    }
  }
}