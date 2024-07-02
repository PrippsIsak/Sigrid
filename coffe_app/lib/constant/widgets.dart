import 'package:flutter/material.dart';

var backgroundColour = Colors.deepOrangeAccent;
var buttonColour = Colors.deepOrangeAccent.shade200;
var appBarBackgroundColour = Colors.deepOrangeAccent[900];
var appBar = AppBar(
                backgroundColor:Colors.deepOrangeAccent,
                title: const Text(
                  textAlign: TextAlign.center,
                  "Sigrid",
                  style: TextStyle(
                    fontStyle: FontStyle.italic,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                centerTitle: true,
              );