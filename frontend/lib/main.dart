import 'package:flutter/material.dart';
import 'video_player_screen.dart';

// Простой Flutter-каркас — Epic 3 (Video player)
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Educational Platform (MVP)',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const VideoPlayerScreen(),
    );
  }
}

