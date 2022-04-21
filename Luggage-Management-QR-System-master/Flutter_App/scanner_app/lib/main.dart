// import ‘package:flutter/cupertino.dart’;
import 'package:flutter/material.dart';
import 'package:barcode_scan/barcode_scan.dart';
import 'package:flutter/services.dart';

import 'api.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  Map<int, Color> color =
  {
    50:Color.fromARGB(255, 20, 40, 80),
    100:Color.fromARGB(255, 20, 40, 80),
    200:Color.fromARGB(255, 20, 40, 80),
    300:Color.fromARGB(255, 20, 40, 80),
    400:Color.fromARGB(255, 20, 40, 80),
    500:Color.fromARGB(255, 20, 40, 80),
    600:Color.fromARGB(255, 20, 40, 80),
    700:Color.fromARGB(255, 20, 40, 80),
    800:Color.fromARGB(255, 20, 40, 80),
    900:Color.fromARGB(255, 20, 40, 80),
  };

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: MaterialColor(0xFF142850, color),
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MyHomePage(title: 'QR Luggage Management App'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  String _result = '';
  String _name = '';
  String _weight = '';
  String _width = '';
  String _height = '';
  String _breadth = '';
  String _container_no = '';
  String _flight = '';

  Future _scan() async {
    try {
      var result = await BarcodeScanner.scan();
      String data = await getData("http://10.0.2.2:5000/api?data=" + result.rawContent);
      var list = data.split(',');
      String name = list[0];
      String weight = list[1];
      String width = list[2];
      String height = list[3];
      String breadth = list[4];
      String container_no = list[5];
      String flight = list[6];

      setState(() {
        _result = result.rawContent;
        _name = name;
        _weight = weight;
        _width = width;
        _height = height;
        _breadth = breadth;
        _container_no = container_no;
        _flight = flight;
      });

    } on PlatformException catch (e) {
      if (e.code == BarcodeScanner.cameraAccessDenied) {
        
      } else {
        
      }
    } on FormatException{
      
    } catch (e) {
      
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Color.fromARGB(255, 39, 73, 109),
      appBar: AppBar(
        title: Text(widget.title),
      ),
      body: Center(     
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: <Widget>[
            Container(
                padding: EdgeInsets.fromLTRB(10,10,10,0),
                height: 220,
                width: double.maxFinite,
                child: Card(
                  color: Color.fromARGB(255, 218, 225, 231),
                  elevation: 5,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: <Widget>[
                      Container(
                        padding: EdgeInsets.fromLTRB(20, 10, 20, 20),
                        child: Text(
                          '$_name',
                          style: TextStyle(
                            fontSize: 30
                          ),
                        ),
                      ),
                      Container(
                        padding: EdgeInsets.fromLTRB(20, 10, 20, 20),
                        child: Text(
                          '$_flight',
                          style: TextStyle(
                            fontSize: 30
                          ),
                        ),
                      ),
                      Container(
                        padding: EdgeInsets.fromLTRB(20, 10, 20, 20),
                        child: Text(
                          'Cargo Hold : $_container_no',
                          style: TextStyle(
                            fontSize: 30
                          ),
                        ),
                      ),
                      
                    ],
                  ),
              ),
            ),
            Container(
                padding: EdgeInsets.fromLTRB(10,0,10,0),
                height: 180,
                width: double.maxFinite,
                child: Card(
                  color: Color.fromARGB(255, 218, 225, 231),
                  elevation: 5,
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: <Widget>[
                      Container(
                        padding: EdgeInsets.fromLTRB(20, 0, 20, 0),
                        child: Text(
                          'Weight : $_weight kg',
                          style: TextStyle(
                            fontSize: 20
                          ),
                        ),
                      ),
                      Container(
                        padding: EdgeInsets.fromLTRB(20, 10, 20, 0),
                        child: Text(
                          'Dimension : $_width x $_height x $_breadth inches',
                          style: TextStyle(
                            fontSize: 20
                          ),
                        ),
                      ),                      
                    ],
                  ),
              ),
            ),
            
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: (_scan),
        tooltip: 'Open Scanner',
        child: Icon(Icons.center_focus_strong),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
