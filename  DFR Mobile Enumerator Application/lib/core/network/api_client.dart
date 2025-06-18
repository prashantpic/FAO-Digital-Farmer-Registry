```dart
import 'package:dio/dio.dart';
import 'package:dfr_mobile/core/config/app_config.dart'; // Placeholder
import 'package:dfr_mobile/injection_container.dart'; // Placeholder

// TODO: Define AppConfig properly and ensure it's loaded to get BASE_API_URL and TIMEOUTS
// For now, using placeholder values or direct constants.
// final AppConfig _appConfig = getIt<AppConfig>();

/// A wrapper around Dio for making HTTP requests to the DFR backend API.
///
/// Configures base URL, timeouts, and interceptors (e.g., for logging,
/// authentication tokens).
class ApiClient {
  final Dio dio;
  static const String _authInterceptorName = 'authInterceptor';

  /// Creates an [ApiClient] instance.
  ///
  /// [baseUrl] is the base URL for all API requests.
  /// It is typically fetched from [AppConfig].
  ApiClient({required String baseUrl, Dio? dioInstance})
      : dio = dioInstance ?? Dio() {
    this.dio.options = BaseOptions(
      baseUrl: baseUrl, // e.g., _appConfig.baseApiUrl
      connectTimeout: const Duration(seconds: 30), // REQ-CONF-003: API_TIMEOUT_SECONDS (connect)
      receiveTimeout: const Duration(seconds: 60), // REQ-CONF-003: API_TIMEOUT_SECONDS (receive)
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    );

    // Add logging interceptor for debugging (consider conditional logging for release)
    // if (kDebugMode) { // Import 'package:flutter/foundation.dart'; for kDebugMode
      this.dio.interceptors.add(LogInterceptor(
            requestBody: true,
            responseBody: true,
            requestHeader: true,
            responseHeader: false,
            error: true,
          ));
    // }
  }

  /// Adds an authentication interceptor to inject the JWT token into request headers.
  ///
  /// [token] is the JWT authentication token.
  void addAuthInterceptor(String token) {
    // Remove existing auth interceptor if any, to prevent multiple auth headers
    removeAuthInterceptor();

    dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) {
        options.headers['Authorization'] = 'Bearer $token';
        return handler.next(options); // Pass the request on
      },
      // Optional: Add onResponse and onError handlers if needed within this interceptor
    )..named(_authInterceptorName)); // Give the interceptor a name
  }

  /// Removes the authentication interceptor.
  ///
  /// Typically called on logout.
  void removeAuthInterceptor() {
    dio.interceptors.removeWhere((interceptor) {
      if (interceptor is InterceptorsWrapper) {
        // This is a naive check. A proper way is to use the named interceptor feature
        // or keep a reference to the interceptor.
        // Dio's InterceptorWrapper does not directly expose a name property after adding.
        // A common pattern is to extend Interceptor and check its type or manage it externally.
        // For simplicity with InterceptorsWrapper, we can rely on removing and re-adding,
        // or manage its presence more carefully.
        // A better approach if using custom Interceptor class:
        // return interceptor is AuthInterceptor;
        // For now, let's assume we ensure only one is added or replace by removing all of type.
        // The `named` extension on Interceptor can help:
        return interceptor.name == _authInterceptorName;
      }
      return false;
    });
  }

  // Example GET request
  Future<Response<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    ProgressCallback? onReceiveProgress,
  }) async {
    try {
      return await dio.get<T>(
        path,
        queryParameters: queryParameters,
        options: options,
        cancelToken: cancelToken,
        onReceiveProgress: onReceiveProgress,
      );
    } on DioException {
      rethrow; // Handled by DfrApiService or repository layer
    }
  }

  // Example POST request
  Future<Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
    CancelToken? cancelToken,
    ProgressCallback? onSendProgress,
    ProgressCallback? onReceiveProgress,
  }) async {
    try {
      return await dio.post<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
        cancelToken: cancelToken,
        onSendProgress: onSendProgress,
        onReceiveProgress: onReceiveProgress,
      );
    } on DioException {
      rethrow; // Handled by DfrApiService or repository layer
    }
  }

  // Add other HTTP methods (PUT, DELETE, PATCH) as needed, following the same pattern.
}

// Extension to name interceptors
extension NamedInterceptor on Interceptor {
  String? get name => _nameMap[this];
  static final _nameMap = <Interceptor, String>{};

  Interceptor named(String name) {
    _nameMap[this] = name;
    return this;
  }
}

// Placeholder for AppConfig if not using getIt for it directly in constructor
// class AppConfig {
//   String get baseApiUrl => "https://your.api.url/api"; // Example
//   // other configs
// }
```