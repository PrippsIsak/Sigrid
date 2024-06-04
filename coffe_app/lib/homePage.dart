import 'package:coffe_app/const.dart';
import 'package:coffe_app/timerPage.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  bool activeAlarms = false;

  @override
  void initState() {
    getActiveAlarms();
    super.initState();
  }

  Future<void> getActiveAlarms() async {
    const String serverUrl = 'http://192.168.0.4:5001/checkActive';

    final response = await http.get(Uri.parse(serverUrl));

    if (response.statusCode == 200) {
      setState(() {
        activeAlarms = json.decode(response.body)['active']; // correct key name
        print(activeAlarms);
      });
    } else {
      print("Failed to fetch alarms");
    }
  }

  void _navigate() {
    Navigator.push(context, MaterialPageRoute(builder: (context) =>
    const TimerPage())
    );
    setState(() {
      getActiveAlarms();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: appBar,
      backgroundColor: backgroundColour,
      body: Padding(
        padding: const EdgeInsets.all(16), // Optional padding
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Row(
              children: [
                GestureDetector(
                  onTap: () {
                   _navigate();
                  },
                  child: Container(
                    alignment: Alignment.center,
                    padding: const EdgeInsets.all(8), // Padding inside the border
                    decoration: BoxDecoration(
                      color: Colors.yellow[100],
                      border: Border.all(
                        color: Colors.blue, // Color of the border
                        width: 2, // Border width
                      ),
                      borderRadius: BorderRadius.circular(8),
                      // Rounded corners
                    ),

                    child: activeAlarms
                        ? Image.asset('lib/images/coffee-machine.png', width: 120, height: 120)
                        : Image.asset('lib/images/coffee-maker.png', width: 120, height: 120),
                  ),
                ),
              ]// Spacing between left and right box
            ),
            // You can add more Rows here for additional content
          ],
        ),
      ),
    );
  }
}
