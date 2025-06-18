import 'package:dfr_mobile/app.dart';
import 'package:dfr_mobile/injection_container.dart' as di; // Dependency Injection
import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart'; // For PlatformDispatcher
// import 'package:dfr_mobile/core/localization/app_localizations.dart'; // For localization init (if needed)
// import 'package:dfr_mobile/core/services/logging_service.dart'; // For global error logging

/// The main entry point for the DFR Mobile Enumerator Application.
///
/// This function initializes essential Flutter bindings, sets up global error handling,
/// configures dependency injection, initializes localization services (if applicable directly here),
/// and then runs the root application widget `App`.
Future<void> main() async {
  // Ensure that Flutter bindings are initialized before any Flutter-specific code.
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize global error handling (Example)
  // This can be expanded to use a logging service.
  PlatformDispatcher.instance.onError = (error, stack) {
    // TODO: Implement more robust global error logging, e.g., using LoggingService
    // final loggingService = di.sl<LoggingService>();
    // loggingService.error('Global unhandled error', error: error, stackTrace: stack);
    debugPrint('Global unhandled error: $error');
    debugPrintStack(stackTrace: stack);
    return true; // Return true to indicate that the error has been handled.
  };

  // Initialize dependency injection container.
  // This will register all services, repositories, usecases, and BLoCs.
  await di.init();

  // Initialize localization services.
  // This might involve loading default locale or other setup if not handled by MaterialApp.
  // For instance, AppLocalizations.load(Locale('en', '')); if needed before runApp.
  // Typically, MaterialApp handles this via delegates.

  // Run the root application widget.
  runApp(const App());
}