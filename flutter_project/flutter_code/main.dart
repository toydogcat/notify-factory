import 'package:flutter/material.dart';
import 'pages/today_page.dart';
/// import 'pages/week_page.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My Info System',

      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        scaffoldBackgroundColor: Colors.blue[50], // 這裡設定背景色
      ),

      home: DefaultTabController(
        length: 2,
        child: Scaffold(
          appBar: AppBar(
            title: const Text('我的資訊系統'),
            bottom: const TabBar(tabs: [
              Tab(text: '今日消息'),
              Tab(text: '這週消息'),
            ]),
          ),
          body: TabBarView(
            children: [TodayPage()],
          ),
          /** body: TabBarView(
            children: [TodayPage(), WeekPage()],
          ), **/
        ),
      ),
      
    );
  }
}