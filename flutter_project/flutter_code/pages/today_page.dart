import 'package:flutter/material.dart';
import '../widgets/tree_menu.dart';
import '../widgets/message_view.dart';
import '../services/data_loader.dart';

class TodayPage extends StatefulWidget {
  @override
  _TodayPageState createState() => _TodayPageState();
}

class _TodayPageState extends State<TodayPage> {
  Map<String, dynamic> todayData = {};
  String selectedRoom = '';
  String selectedSource = '';

  @override
  void initState() {
    super.initState();
    loadTodayJson().then((data) {
      setState(() => todayData = data);
    });
  }

  void refreshData() async {
    // bool isNewDay = await checkIfNewDay();
    bool isNewDay = false;
    if (isNewDay) {
      await updateWeekDb();
    }
    var data = await loadTodayJson();
    setState(() => todayData = data);
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          flex: 2,
          child: Column(
            children: [
              ElevatedButton(onPressed: refreshData, child: Text("重新整理")),
              Expanded(
                child: TreeMenu(
                  data: todayData['rooms'] ?? {},
                  onSelect: (room, source) {
                    setState(() {
                      selectedRoom = room;
                      selectedSource = source;
                    });
                  },
                ),
              ),
            ],
          ),
        ),
        Expanded(
          flex: 5,
          child: MessageView(
            entries: todayData['rooms']?[selectedRoom]?[selectedSource] ?? [],
          ),
        ),
      ],
    );
  }
}
