import 'package:flutter/material.dart';
/// import 'pages/today_page.dart';
/// import 'pages/week_page.dart';

void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My Info System',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
      ),
      home: DefaultTabController(
        length: 2,
        child: Scaffold(
          appBar: AppBar(
            title: Text('我的資訊系統'),
            bottom: TabBar(tabs: [
              Tab(text: '今日消息'),
              Tab(text: '這週消息'),
            ]),
          ),
          /** body: TabBarView(
            children: [TodayPage(), WeekPage()],
          ), **/
        ),
      ),
    );
  }
}