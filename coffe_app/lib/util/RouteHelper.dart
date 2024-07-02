import 'package:flutter/material.dart';
import 'package:coffe_app/createTimerPage.dart';
import 'package:coffe_app/homePage.dart';
import 'package:coffe_app/loginPage.dart';
import 'package:coffe_app/constant/Constant.dart';

class RouteHelper {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case homeRoute:
        return MaterialPageRoute(builder: (_) => const HomePage());
      case loginRoute:
        return MaterialPageRoute(
            builder: (_) => const LoginPage(
                  title: '',
                ));
      case createTimerRoute:
        return MaterialPageRoute(builder: (_) => const CreateTimerPage());
        
      default:
        return MaterialPageRoute(
            builder: (_) => Scaffold(
                  body: Center(
                      child: Text('No route defined for ${settings.name}')),
                ));
    }
  }
}
