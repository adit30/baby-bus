import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(RobotControlApp());
}

class RobotControlApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: RobotControlPage(),
    );
  }
}

class RobotControlPage extends StatefulWidget {
  @override
  _RobotControlPageState createState() => _RobotControlPageState();
}

class _RobotControlPageState extends State<RobotControlPage> {
  String _status = 'Stopped';

  void _sendCommand(String command) async {
    final url = Uri.parse('http://192.168.0.168:5001'); // Replace with your robot's IP address

    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: '{"movement": "$command"}',
      );

      if (response.statusCode == 200) {
        setState(() {
          _status = 'Moving $command';
        });
      } else {
        setState(() {
          _status = 'Failed to send command';
        });
      }
    } catch (e) {
      setState(() {
        _status = 'Error: $e';
      });
    }
  }

  void _stopCommand() {
    _sendCommand('stop');
    setState(() {
      _status = 'Stopped';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Ayesha's Baby Bus"),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text('Status: $_status'),
            SizedBox(height: 20),
            Column(
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    buildButton('rotate_left', Icons.rotate_left, 'Rotate Left'),
                    buildButton('forward', Icons.arrow_upward, 'Forward'),
                    buildButton('rotate_right', Icons.rotate_right, 'Rotate Right'),
                  ],
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    buildButton('left', Icons.arrow_back, 'Left'),
                    buildButton('stop', Icons.stop, 'Stop'),
                    buildButton('right', Icons.arrow_forward, 'Right'),
                  ],
                ),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    buildButton('spin_left', Icons.rotate_left, 'Spin Left'),
                    buildButton('backward', Icons.arrow_downward, 'Backward'),
                    buildButton('spin_right', Icons.rotate_right, 'Spin Right'),
                  ],
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget buildButton(String command, IconData icon, String label) {
    return GestureDetector(
      onTapDown: (_) {
        _sendCommand(command);
      },
      onTapUp: (_) {
        _stopCommand();
      },
      child: Column(
        children: [
          Icon(
            icon,
            size: 80, // Adjust the size as needed
            color: Colors.blue,
          ),
          SizedBox(height: 8),
          Text(label),
        ],
      ),
    );
  }
}
