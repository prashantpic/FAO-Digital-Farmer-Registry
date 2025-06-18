import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';

/// Service to provide information about the device's network connectivity status.
///
/// This service uses the `connectivity_plus` plugin to check for active
/// internet connections (Wi-Fi, Mobile Data) and to listen for changes
/// in connectivity status. This is crucial for implementing offline-first
/// behavior and scheduling data synchronization.
class ConnectivityService {
  final Connectivity _connectivity;

  /// Creates an instance of [ConnectivityService].
  ///
  /// Optionally, a [Connectivity] instance can be provided for testing,
  /// otherwise a default instance is created.
  ConnectivityService({Connectivity? connectivity})
      : _connectivity = connectivity ?? Connectivity();

  /// Checks if the device currently has an active internet connection.
  ///
  /// An active connection is considered to be either Wi-Fi or Mobile Data.
  /// Returns `true` if connected, `false` otherwise.
  Future<bool> isConnected() async {
    final connectivityResult = await _connectivity.checkConnectivity();
    // Prior to Dart 3, contains was not on List<Enum>, so using a loop or .any
    // Modern Dart allows contains directly on List<ConnectivityResult>
    #if SDK_VERSION_AT_LEAST_3_0_0
      return connectivityResult.contains(ConnectivityResult.mobile) ||
             connectivityResult.contains(ConnectivityResult.wifi) ||
             connectivityResult.contains(ConnectivityResult.ethernet); // Added ethernet as per connectivity_plus
    #else
      // Fallback for older Dart versions if necessary, though Flutter 3.22.2 uses Dart 3.4.3
      return _isConnected(connectivityResult);
    #endif
  }

  /// Helper method for checking connectivity, compatible with older list checks if needed.
  bool _isConnected(List<ConnectivityResult> result) {
    return result.any((r) => r == ConnectivityResult.mobile || r == ConnectivityResult.wifi || r == ConnectivityResult.ethernet);
  }


  /// A stream that emits [ConnectivityResult] whenever the network connectivity changes.
  ///
  /// This can be used to reactively update UI or application behavior based on
  /// network status.
  ///
  /// Example usage:
  /// ```dart
  /// connectivityService.onConnectivityChanged.listen((ConnectivityResult result) {
  ///   if (result == ConnectivityResult.none) {
  ///     // Handle offline state
  ///   } else {
  ///     // Handle online state
  ///   }
  /// });
  /// ```
  Stream<List<ConnectivityResult>> get onConnectivityChanged => _connectivity.onConnectivityChanged;

  /// A stream that emits a boolean value indicating connectivity status (true for connected, false for disconnected).
  /// This is a convenience stream derived from `onConnectivityChanged`.
  Stream<bool> get onConnectivityStatusChanged {
    return _connectivity.onConnectivityChanged.map((result) {
      #if SDK_VERSION_AT_LEAST_3_0_0
        return result.contains(ConnectivityResult.mobile) ||
               result.contains(ConnectivityResult.wifi) ||
               result.contains(ConnectivityResult.ethernet);
      #else
        return _isConnected(result);
      #endif
    });
  }
}