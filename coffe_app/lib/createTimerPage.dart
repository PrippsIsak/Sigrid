import 'dart:convert';
import 'package:coffe_app/constant/routes.dart';
import 'package:coffe_app/constant/widgets.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class CreateTimerPage extends StatefulWidget {
  const CreateTimerPage({super.key});

  @override
  State<CreateTimerPage> createState() => _CreateTimerPageState();
}

class _CreateTimerPageState extends State<CreateTimerPage> {
  final TextEditingController _hourController = TextEditingController();
  final TextEditingController _minuteController = TextEditingController();

  void _createTimer() {
    int hour = int.parse(_hourController.text);
    int minute = int.parse(_minuteController.text);
    const String apiUrl = "http://192.168.0.4:5001/createAlarm";

    final Map<String, int> payload = {
      'hour': hour,
      'minute': minute,
    };

    http
        .post(
      Uri.parse(apiUrl),
      headers: <String, String>{
        'Content-type': 'application/json',
      },
      body: jsonEncode(payload),
    )
        .then((response) {
      if (response.statusCode != 200) {
        Navigator.pushNamed(context, Routes.badRequestRoute);
      } else {
        Navigator.pop(context);
      }
    }).catchError((error) {
      print("Error:  $error");
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: backgroundColour,
      appBar: appBar,
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            TextField(
              controller: _hourController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(labelText: 'Hour'),
            ),
            SizedBox(
              height: 16,
            ),
            TextField(
              controller: _minuteController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(labelText: 'Minute'),
            ),
            const SizedBox(
              height: 16,
            ),
            ElevatedButton(onPressed: _createTimer, child: Text('Add Timer'))
          ],
        ),
      ),
    );
  }
}
