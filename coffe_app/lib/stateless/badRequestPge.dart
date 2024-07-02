import 'package:flutter/material.dart';
import 'package:coffe_app/constant/widgets.dart'; // Assuming this is your constants import

class BadRequestPage extends StatelessWidget {
  const BadRequestPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: appBar,
      body: Container(
        alignment: Alignment.center,
        color: Colors.deepOrangeAccent[600],
        constraints: BoxConstraints(
          maxHeight: 100,
          maxWidth: 50,
        ),
        child: const Text(
          'Opps! Bad request!',
          style: TextStyle(
            fontSize: 16,
            fontStyle: FontStyle.italic,
          ),
        ),
      ),
    );
  }
}
