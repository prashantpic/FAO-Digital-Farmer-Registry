import 'package:flutter/material.dart';

/// Defines the application's visual themes, including color schemes,
/// typography, and component styling, adhering to Material Design guidelines.
///
/// This class provides static `ThemeData` objects for light and dark themes,
/// ensuring a consistent look and feel across the application.
class AppTheme {
  AppTheme._(); // Private constructor to prevent instantiation.

  // Placeholder primary color. Replace with actual DFR branding color.
  static const Color _primaryColor = Color(0xFF00695C); // Example: A teal variant
  static const Color _accentColor = Color(0xFFFFA000); // Example: An amber variant

  /// The light theme for the application.
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      primaryColor: _primaryColor,
      colorScheme: ColorScheme.fromSeed(
        seedColor: _primaryColor,
        brightness: Brightness.light,
        secondary: _accentColor,
      ),
      scaffoldBackgroundColor: Colors.grey[100],
      appBarTheme: AppBarTheme(
        backgroundColor: _primaryColor,
        foregroundColor: Colors.white,
        elevation: 4.0,
        titleTextStyle: const TextStyle(
          color: Colors.white,
          fontSize: 20,
          fontWeight: FontWeight.w500,
        ),
      ),
      textTheme: _textTheme(ThemeData.light().textTheme),
      inputDecorationTheme: _inputDecorationTheme(Brightness.light),
      elevatedButtonTheme: _elevatedButtonTheme(_primaryColor),
      textButtonTheme: _textButtonTheme(_primaryColor),
      floatingActionButtonTheme: FloatingActionButtonThemeData(
        backgroundColor: _accentColor,
        foregroundColor: Colors.black,
      ),
      // Add other component themes as needed
    );
  }

  /// The dark theme for the application.
  /// This can be enabled via a feature toggle (REQ-CONF-001 enableDarkTheme).
  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      primaryColor: _primaryColor, // Or a dark theme adjusted primary
      colorScheme: ColorScheme.fromSeed(
        seedColor: _primaryColor,
        brightness: Brightness.dark,
        secondary: _accentColor, // Or a dark theme adjusted accent
      ),
      scaffoldBackgroundColor: Colors.grey[850],
      appBarTheme: AppBarTheme(
        backgroundColor: Colors.grey[900],
        foregroundColor: Colors.white,
        elevation: 4.0,
        titleTextStyle: const TextStyle(
          color: Colors.white,
          fontSize: 20,
          fontWeight: FontWeight.w500,
        ),
      ),
      textTheme: _textTheme(ThemeData.dark().textTheme),
      inputDecorationTheme: _inputDecorationTheme(Brightness.dark),
      elevatedButtonTheme: _elevatedButtonTheme(_accentColor), // Dark theme might use accent for buttons
      textButtonTheme: _textButtonTheme(_accentColor),
      floatingActionButtonTheme: FloatingActionButtonThemeData(
        backgroundColor: _accentColor,
        foregroundColor: Colors.black,
      ),
      // Add other component themes as needed
    );
  }

  static TextTheme _textTheme(TextTheme base) {
    return base.copyWith(
      headlineSmall: base.headlineSmall?.copyWith(fontWeight: FontWeight.w500),
      titleLarge: base.titleLarge?.copyWith(fontSize: 18.0, fontWeight: FontWeight.bold),
      bodyMedium: base.bodyMedium?.copyWith(fontSize: 16.0),
      labelLarge: base.labelLarge?.copyWith(fontWeight: FontWeight.w600, fontSize: 14.0),
    ).apply(
      fontFamily: 'Roboto', // Example font, replace if custom fonts are used
    );
  }

  static InputDecorationTheme _inputDecorationTheme(Brightness brightness) {
    final borderColor = brightness == Brightness.light ? _primaryColor : _accentColor;
    return InputDecorationTheme(
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8.0),
        borderSide: BorderSide(color: borderColor.withOpacity(0.5)),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8.0),
        borderSide: BorderSide(color: borderColor.withOpacity(0.7)),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8.0),
        borderSide: BorderSide(color: borderColor, width: 2.0),
      ),
      errorBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8.0),
        borderSide: BorderSide(color: Colors.red.shade700, width: 1.5),
      ),
      focusedErrorBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(8.0),
        borderSide: BorderSide(color: Colors.red.shade700, width: 2.0),
      ),
      filled: true,
      fillColor: brightness == Brightness.light ? Colors.white : Colors.grey[800],
      contentPadding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 12.0),
    );
  }

  static ElevatedButtonThemeData _elevatedButtonTheme(Color buttonColor) {
    return ElevatedButtonThemeData(
      style: ElevatedButton.styleFrom(
        backgroundColor: buttonColor,
        foregroundColor: Colors.white, // Text color
        padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 12.0),
        textStyle: const TextStyle(fontSize: 16.0, fontWeight: FontWeight.w500),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8.0),
        ),
        elevation: 2,
      ),
    );
  }

  static TextButtonThemeData _textButtonTheme(Color buttonColor) {
    return TextButtonThemeData(
      style: TextButton.styleFrom(
        foregroundColor: buttonColor, // Text color
        padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 10.0),
        textStyle: const TextStyle(fontSize: 16.0, fontWeight: FontWeight.w500),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8.0),
        ),
      ),
    );
  }
}

/// DFR specific colors (placeholder, to be defined based on branding).
/// This can be expanded into a full color palette.
class DFRColors {
 DFRColors._();
 static const Color primary = AppTheme._primaryColor;
 static const Color accent = AppTheme._accentColor;
 // Add more DFR specific colors here
}