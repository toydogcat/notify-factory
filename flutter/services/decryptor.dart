import 'package:encrypt/encrypt.dart' as enc;

String decryptContent(String encryptedText, String password) {
  final key = enc.Key.fromUtf8(password.padRight(32, '0'));
  final iv = enc.IV.fromLength(16);
  final encrypter = enc.Encrypter(enc.AES(key));
  return encrypter.decrypt(enc.Encrypted.fromBase64(encryptedText), iv: iv);
}
