import 'dart:convert';
import 'package:flutter/services.dart' show rootBundle;
import 'package:intl/intl.dart';

Future<Map<String, dynamic>> loadTodayJson() async {
  final jsonString = await rootBundle.loadString('assets/today.json');
  return json.decode(jsonString);
}

// 模擬：檢查是否為新的一天（實際應該比對本地快取或資料庫）
Future<bool> checkIfNewDay() async {
  // 假設今天是 2025-07-10
  final now = DateTime.now();
  final today = DateFormat('yyyy-MM-dd').format(now);
  // 這裡可以改成讀取本地快取的日期
  return true; // 總是當作新的一天（測試用）
}

// 模擬：更新 week.db（實際應該呼叫 API 或下載檔案）
Future<void> updateWeekDb() async {
  // TODO: 加入下載或更新邏輯
  print("更新 week.db 與 today.json");
}
