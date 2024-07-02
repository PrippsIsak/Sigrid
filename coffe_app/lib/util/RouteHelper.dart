import 'package:coffe_app/listPage.dart';
import 'package:coffe_app/stateless/badRequestPge.dart';
import 'package:coffe_app/timerPage.dart';
import 'package:flutter/material.dart';
import 'package:coffe_app/createTimerPage.dart';
import 'package:coffe_app/homePage.dart';
import 'package:coffe_app/loginPage.dart';
import 'package:coffe_app/constant/routes.dart';

class RouteHelper {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case Routes.homeRoute:
        return MaterialPageRoute(builder: (_) => const HomePage());
      case Routes.loginRoute:
        return MaterialPageRoute(
            builder: (_) => const LoginPage(
                  title: '',
                ));
      case Routes.createTimerRoute:
        return MaterialPageRoute(builder: (_) => const CreateTimerPage());
      case Routes.shoppingListRoute:
        return MaterialPageRoute(builder: (_) => const ListPage());
      case Routes.badRequestRoute:
        return MaterialPageRoute(builder: (_) => const BadRequestPage());
      case Routes.timerPageRoute:
        return MaterialPageRoute(builder: (_) => const TimerPage());
      default:
        return MaterialPageRoute(
            builder: (_) => Scaffold(
                  body: Center(
                      child: Text('No route defined for ${settings.name}')),
                ));
    }
  }
}
