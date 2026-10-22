import 'package:http/http.dart' as http;

class ApiService{
 String baseUrl = 'http://127.0.0.1:8000';
 Future<String>  getAssigments() async{
  String getAssigmentUrl = "$baseUrl/assignments"; 
  var response = await http.get(Uri.parse(getAssigmentUrl));

  if (response.statusCode == 200){
    return response.body;
  }
  else{
    return "Error:${response.statusCode}";
  }
  
 }
}

