import 'dart:convert';

import 'package:coffe_app/const.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class ListPage extends StatefulWidget {
  const ListPage({super.key});

  @override
  State<ListPage> createState() => _ListPageState();
}

class _ListPageState extends State<ListPage> {
  final TextEditingController _listItemController = TextEditingController();
  List<dynamic> _shoppingList = [];

  @override
  void initState() {
    super.initState();
    _fetchList();
  }

  void _navigate(Widget page) {
    Navigator.push(context, MaterialPageRoute(builder: (context) => page));
  }

  Future<void> _fetchList() async {
    try {
      const String apiUrl = "http://192.168.0.4:5001/getShoppingItems";
      final response = await http.get(Uri.parse(apiUrl));

      if (response.statusCode == 200) {
        setState(() {
          _shoppingList = json.decode(response.body)["Shopping items"];
        });
      } else {
        //TODO: fix better logic,
      }
    } catch (error) {}
  }

  Future<void> _deletedItems() async {
    List<dynamic> toBeDeleted = [];
    for (int i = 0; i < _shoppingList.length; i++) {
      if (_shoppingList[i]['checked']) {
        toBeDeleted.add(_shoppingList[i]);
        _shoppingList.removeAt(i);
      }
    }
    if (toBeDeleted.isNotEmpty) {
      try {
        const String apiUrl = "http://192.168.0.4:5001/deleteShoppingItems";
        http
            .post(Uri.parse(apiUrl),
                headers: <String, String>{
                  'Content-Type': 'application/json',
                },
                body: json.encode(toBeDeleted))
            .then((response) {})
            .catchError((error) {});
      } catch (error) {}
    }
  }

  Future<void> _addItem() async {
    String? newItem = await showDialog(
        context: context,
        builder: (BuildContext context) {
          return AlertDialog(
            title: const Text('Add shopping item'),
            content: TextField(
              controller: _listItemController,
            ),
            actions: <Widget>[
              TextButton(
                  onPressed: () {
                    Navigator.of(context).pop(_listItemController.text);
                  },
                  child: const Text('Add')),
              TextButton(
                  onPressed: () {
                    Navigator.of(context).pop();
                  },
                  child: const Text('Cancel'))
            ],
          );
        });
    if (newItem != null && newItem.isNotEmpty) {
      setState(() {
        _createItem(newItem);
        _listItemController.clear();
        _fetchList();
      });
    }
  }

  Future<void> _createItem(String itemName) async {
    Map<String, dynamic> body = {'shoppingItem': itemName, 'checked': false};

    try {
      String apiUrl = "http://192.168.0.4:5001/createShoppingItems";
      final response = await http
          .post(
        Uri.parse(apiUrl),
        headers: <String, String>{
          'Content-Type': 'application/json',
        },
        body: jsonEncode(body),
      )
          .then((response) {
        //TODO: fix later
      }).catchError((onError) {});
    } catch (error) {}
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: appBar,
      backgroundColor: backgroundColour,
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(children: [
          Expanded(
              child: ListView.builder(
                  itemCount: _shoppingList.length,
                  itemBuilder: (context, index) {
                    String item = "${_shoppingList[index]['shoppingItem']}";
                    bool isChecked = _shoppingList[index]['checked'];
                    return Column(
                      children: [
                        ListTile(
                          title: Text(
                            item,
                            style: const TextStyle(fontSize: 20),
                            textAlign: TextAlign.center,
                          ),
                          trailing: Checkbox(
                            value: isChecked,
                            onChanged: (bool? value) {
                              setState(() {
                                _shoppingList[index]['checked'] = value;
                              });
                            },
                            activeColor: Colors.green,
                          ),
                        )
                      ],
                    );
                  })),
          PopupMenuButton(
            onSelected: (value) {
              if (value == 0) {
                setState(() {
                  _addItem();
                });
              }
              if (value == 1) {
                _deletedItems();
              }
            },
            itemBuilder: (BuildContext context) => [
              const PopupMenuItem(value: 0, child: Text('Add item')),
              const PopupMenuItem(value: 1, child: Text('Remove checked item')),
            ],
            icon: const Icon(
              Icons.account_tree_rounded,
              size: 40,
            ),
          ),
        ]),
      ),
    );
  }
}
