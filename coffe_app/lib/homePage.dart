import 'package:coffe_app/constant/widgets.dart';
import 'package:coffe_app/loginPage.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:coffe_app/constant/routes.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> with RouteAware {
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
        activeAlarms = json.decode(response.body)['active']; 
      });
    } else {
      Navigator.pushNamed(context, Routes.badRequestRoute);
    }
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    final ModalRoute? modalRoute = ModalRoute.of(context);
    if (modalRoute is PageRoute) {
      routeObserver.subscribe(this, modalRoute);
    }
  }

  @override
  void dispose() {
    routeObserver.unsubscribe(this);
    super.dispose();
  }

  @override
  void didPopNext() {
    getActiveAlarms();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: appBar,
      backgroundColor: backgroundColour,
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment
                  .spaceEvenly,
              children: [
                GestureDetector(
                  onTap: () {
                    Navigator.pushNamed(context, Routes.timerPageRoute);
                  },
                  child: Container(
                    alignment: Alignment.center,
                    padding:
                        const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: Colors.yellow[100],
                      border: Border.all(
                        color: Colors.blue,
                        width: 2, 
                      ),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: activeAlarms
                        ? Image.asset('lib/images/coffee-machine.png',
                            width: 120, height: 120)
                        : Image.asset('lib/images/coffee-maker.png',
                            width: 120, height: 120),
                  ),
                ),
                GestureDetector(
                  onTap: () {
                      Navigator.pushNamed(context, Routes.shoppingListRoute);
                  },
                  child: Container(
                    alignment: Alignment.center,
                    padding:
                        const EdgeInsets.all(8), 
                    decoration: BoxDecoration(
                      color: Colors.yellow[100],
                      border: Border.all(
                        color: Colors.blue,
                        width: 2, 
                      ),
                      borderRadius: BorderRadius.circular(8),                    
                    ),
                    child: Image.asset('lib/images/list.jpg',
                        width: 120, height: 120), 
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
