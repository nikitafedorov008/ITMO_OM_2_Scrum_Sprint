import 'package:flutter/material.dart';
import 'package:video_player/video_player.dart';

// Video player screen — каркас для Epic 3
// Здесь использован плагин `video_player` (Flutter-эквивалент интеграции видео-плеера).
// В веб-версии можно интегрировать video.js через webview или web-пакет.

class VideoPlayerScreen extends StatefulWidget {
  const VideoPlayerScreen({super.key});

  @override
  State<VideoPlayerScreen> createState() => _VideoPlayerScreenState();
}

class _VideoPlayerScreenState extends State<VideoPlayerScreen> {
  late VideoPlayerController _controller;
  bool _initialized = false;

  @override
  void initState() {
    super.initState();
    // Пример network-ролика. В реальном приложении брать ссылку из backend/courses
    _controller = VideoPlayerController.network(
      'https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4',
    )
      ..initialize().then((_) {
        setState(() {
          _initialized = true;
        });
      });
    _controller.setLooping(true);
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Видео-плеер — Epic 3'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            if (_initialized)
              AspectRatio(
                aspectRatio: _controller.value.aspectRatio,
                child: VideoPlayer(_controller),
              )
            else
              const CircularProgressIndicator(),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                setState(() {
                  _controller.value.isPlaying
                      ? _controller.pause()
                      : _controller.play();
                });
              },
              child: Icon(
                _controller.value.isPlaying ? Icons.pause : Icons.play_arrow,
              ),
            ),
            const SizedBox(height: 12),
            const Text('Пример экрана с плеером. Связан с Epic 3.'),
          ],
        ),
      ),
    );
  }
}

