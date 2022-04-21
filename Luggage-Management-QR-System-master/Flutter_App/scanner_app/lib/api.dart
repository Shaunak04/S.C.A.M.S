import 'package:http/http.dart' as http;

Future getData(url) async {
  http.Response resp = await http.get(url);
  return resp.body;
}