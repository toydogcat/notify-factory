import 'package:flutter/material.dart';
import '../services/decryptor.dart';

class DecryptBox extends StatefulWidget {
  final String encryptedText;

  DecryptBox({required this.encryptedText});

  @override
  _DecryptBoxState createState() => _DecryptBoxState();
}

class _DecryptBoxState extends State<DecryptBox> {
  String password = '';
  String decrypted = '';
  bool showPassword = false;

  void decrypt() {
    try {
      decrypted = decryptContent(widget.encryptedText, password);
    } catch (e) {
      decrypted = '[解密失敗]';
    }
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          children: [
            Expanded(
              child: TextField(
                obscureText: !showPassword,
                onChanged: (val) => password = val,
                decoration: InputDecoration(labelText: '密碼'),
              ),
            ),
            IconButton(
              icon: Icon(showPassword ? Icons.visibility : Icons.visibility_off),
              onPressed: () => setState(() => showPassword = !showPassword),
            ),
            ElevatedButton(onPressed: decrypt, child: Text("解密"))
          ],
        ),
        if (decrypted.isNotEmpty) Text(decrypted),
      ],
    );
  }
}
