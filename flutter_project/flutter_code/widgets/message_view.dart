import 'package:flutter/material.dart';
import '../widgets/decrypt_box.dart';

class MessageView extends StatelessWidget {
  final List<dynamic> entries;

  const MessageView({super.key, required this.entries});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: entries.length,
      itemBuilder: (context, index) {
        var entry = entries[index];
        return Card(
          child: ListTile(
            title: Text(entry['title']),
            subtitle: entry['encrypted'] == true
                ? DecryptBox(encryptedText: entry['content'])
                : Text(entry['content']),
          ),
        );
      },
    );
  }
}
