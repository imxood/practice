import 'package:flutter/material.dart';

class IicPage extends StatefulWidget {
  IicPage({Key key}) : super(key: key);

  @override
  _IicPageState createState() => _IicPageState();
}

class _IicPageState extends State<IicPage> {
  var isMaster = true;
  @override
  Widget build(BuildContext context) {
    var masterBtn = Container(
      decoration: BoxDecoration(
        border: Border(bottom: BorderSide(width: 5, color: Colors.red)),
      ),
      child: TextButton(
        child: Text(
          "Master",
          style: TextStyle(),
        ),
        onPressed: () {
          setState(() {
            isMaster = true;
          });
          print("master view is clicked");
        },
      ),
    );

    var slaveBtn = Container(
      child: TextButton(
        child: Text("Slave"),
        onPressed: () {
          print("slave view is clicked");
          setState(() {
            isMaster = false;
          });
        },
      ),
    );

    var header = Stack(
      alignment: Alignment.bottomRight,
      children: [
        Container(
          width: double.infinity,
          color: Colors.black12,
          child: Align(
            alignment: Alignment.topLeft,
            child: Text(
              "I2C Control",
              style: TextStyle(
                fontSize: 45,
                color: Colors.black87,
              ),
            ),
          ),
        ),
        Wrap(
          children: [
            Container(
              child: masterBtn,
            ),
            SizedBox(width: 5),
            Container(
              child: slaveBtn,
            ),
          ],
        )
      ],
    );

    var masterView = Container(
      height: 100,
      child: Text("masterView"),
    );

    var slaveView = Container(
      height: 100,
      child: Text("slaveView"),
    );

    var tabView = TabBarView(
      children: [
        masterView,
        slaveView,
      ],
    );

    return Container(
      height: 400,
      child: Column(
        children: [
          header,
          if (isMaster) masterView,
        ],
      ),
    );
  }
}
