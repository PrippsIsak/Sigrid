import 'dart:convert';
import 'dart:ffi';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:coffe_app/constant/routes.dart';
import 'package:coffe_app/constant/widgets.dart';

class TimerPage extends StatefulWidget {
  const TimerPage({Key? key}) : super(key: key);

  @override
  _TimerPageState createState() => _TimerPageState();
}

class _TimerPageState extends State<TimerPage> {
  final TextEditingController _hourController = TextEditingController();
  final TextEditingController _minuteController = TextEditingController();
  List<dynamic> _alarms = [];

  @override
  void initState() {
    super.initState();
    fetchAlarms();
  }

  void _navigate(Widget page) {
    Navigator.push(context, MaterialPageRoute(builder: (context) => page));
  }

  Future<void> fetchAlarms() async {
    try {
      const String apiUrl = "http://192.168.0.4:5001/getAllAlarms";
      final response = await http.get(Uri.parse(apiUrl));

      if (response.statusCode == 200) {
        setState(() {
          print("Response body: ${response.body}");
          _alarms = json.decode(response.body)["Alarms"];
          print(_alarms);
        });
      } else {
        Navigator.pushNamed(context, Routes.badRequestRoute);
      }
    } catch (error) {
      print("Error: $error");
    }
  }

  void _coffeOnOff(bool state) {
    const String serverUrl = 'http://192.168.0.4:5001/toggleCoffee';

    Map<String, dynamic> body = {'state': state};

    http
        .post(Uri.parse(serverUrl),
            headers: <String, String>{'Content-Type': 'application/json'},
            body: jsonEncode(body),
            ).then((response) {
      if (response.statusCode == 400) {
        Navigator.pushNamed(context, Routes.badRequestRoute);
      } else if (response.statusCode == 500) {
        //TODO drop down message that says that coffe machine could not turn on
      }
    }).catchError((onError) {
      print(onError);
    });
  }

  void _toggleOnOff(int hour, int minute, bool state) {
    // Update the URL with your Python server endpoint
    const String serverUrl = 'http://192.168.0.4:5001/toggleAlarm';

    //create payload
    Map<String, dynamic> body = {
      'hour': hour,
      'minute': minute,
      'active': state
    };

    // Make a POST request to your Python server with the JSON body
    http
        .post(
      Uri.parse(serverUrl),
      headers: <String, String>{
        'Content-Type': 'application/json',
      },
      body: jsonEncode(body), // Encode the body as JSON
    )
        .then((response) {
      // Handle the response from the server if needed
      print('Server response: ${response.body}');
    }).catchError((error) {
      // Handle errors
      print('Error: $error');
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: appBar,
      backgroundColor: backgroundColour,
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Expanded(
                child: ListView.builder(
              itemCount: _alarms.length,
              itemBuilder: (context, index) {
                String time =
                    "${_alarms[index]['hour']}:${_alarms[index]['minute']}";
                return Column(children: [
                  ListTile(
                    title: Text(
                      time,
                      style: const TextStyle(fontSize: 20),
                      textAlign: TextAlign.center,
                    ),
                    onTap: () {
                      setState(() {
                        _alarms[index]['active'] = !_alarms[index]['active'];
                        _toggleOnOff(_alarms[index]['hour'],
                            _alarms[index]['minute'], _alarms[index]['active']);
                      });
                    },
                    contentPadding: const EdgeInsets.symmetric(
                        horizontal: 16.0, vertical: 8.0),

                    tileColor: _alarms[index]['active']
                        ? Colors.green.shade400
                        : Colors.white70,
                    titleAlignment: ListTileTitleAlignment.center,
                    //onTap: _,
                  ),
                  const Divider(),
                ]);
              },
            )),
            //TODO: fix better popupMenu
            PopupMenuButton(
              onSelected: (value) {
                if (value == 0) {
                  Navigator.pushNamed(context, Routes.createTimerRoute);
                }
                if (value == 1) {
                  _coffeOnOff(true);
                }
              },
              itemBuilder: (BuildContext context) => [
                const PopupMenuItem(value: 0, child: Text('Add coffee alarm')),
                const PopupMenuItem(value: 1, child: Text('Turn on coffe'))
              ],
              icon: const Icon(Icons.account_circle_sharp, size: 40),
            ),
          ],
        ),
      ),
    );
  }
}
