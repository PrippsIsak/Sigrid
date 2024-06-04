import 'dart:ui';

class BoxData {
  final String title;  // Title displayed on the box
  final Color color;   // Background color of the box
  final VoidCallback onTap;  // Function to be called when the box is tapped

  const BoxData({required this.title, required this.color, required this.onTap});
}