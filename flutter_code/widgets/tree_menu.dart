import 'package:flutter/material.dart';

class TreeMenu extends StatelessWidget {
  final Map<String, dynamic> data;
  final Function(String, String) onSelect;

  TreeMenu({required this.data, required this.onSelect});

  @override
  Widget build(BuildContext context) {
    return ListView(
      children: data.entries.map((roomEntry) {
        return ExpansionTile(
          title: Text(roomEntry.key),
          children: (roomEntry.value as Map<String, dynamic>).keys.map((source) {
            return ListTile(
              title: Text(source),
              onTap: () => onSelect(roomEntry.key, source),
            );
          }).toList(),
        );
      }).toList(),
    );
  }
}
