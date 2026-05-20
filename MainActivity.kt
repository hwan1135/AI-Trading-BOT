package com.example.aitrader

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(modifier = Modifier.fillMaxSize(), color = MaterialTheme.colorScheme.background) {
                    TraderDashboard()
                }
            }
        }
    }
}

// Replace with your computer's local IP (e.g., 192.168.1.X) or Cloud IP
const val SERVER_URL = "http://10.0.2.2:8000" 

@Composable
fun TraderDashboard() {
    var isSystemActive by remember { mutableStateOf(false) }
    var logs by remember { mutableStateOf(listOf<String>()) }
    var portfolioCount by remember { mutableStateOf(0) }
    val coroutineScope = rememberCoroutineScope()

    // Background loop to fetch status every 3 seconds
    LaunchedEffect(Unit) {
        while (true) {
            val status = fetchServerData("/api/status")
            if (status != null) {
                isSystemActive = status.getBoolean("active")
                val logArray = status.getJSONArray("logs")
                val newLogs = mutableListOf<String>()
                for (i in 0 until logArray.length()) { newLogs.add(logArray.getString(i)) }
                logs = newLogs
            }
            delay(3000)
        }
    }

    Column(modifier = Modifier.padding(16.dp)) {
        Text("AI Auto-Trader Dashboard", style = MaterialTheme.typography.headlineMedium)
        Spacer(modifier = Modifier.height(16.dp))

        // Control Panel
        Card(modifier = Modifier.fillMaxWidth(), colors = CardDefaults.cardColors(
            containerColor = if (isSystemActive) Color(0xFFD4EDDA) else Color(0xFFF8D7DA)
        )) {
            Column(modifier = Modifier.padding(16.dp)) {
                Text("System Status: ${if (isSystemActive) "ONLINE & SCANNING" else "OFFLINE"}")
                Spacer(modifier = Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.SpaceEvenly, modifier = Modifier.fillMaxWidth()) {
                    Button(onClick = { 
                        coroutineScope.launch { sendCommand("start") } 
                    }, enabled = !isSystemActive) { Text("ENGAGE AI") }
                    
                    Button(onClick = { 
                        coroutineScope.launch { sendCommand("stop") } 
                    }, enabled = isSystemActive, colors = ButtonDefaults.buttonColors(containerColor = Color.Red)) { 
                        Text("HALT TRADING") 
                    }
                }
            }
        }

        Spacer(modifier = Modifier.height(24.dp))
        Text("Activity Logs", style = MaterialTheme.typography.titleLarge)
        Divider(modifier = Modifier.padding(vertical = 8.dp))

        // Log Viewer
        LazyColumn(modifier = Modifier.fillMaxSize()) {
            items(logs) { log ->
                Text(log, modifier = Modifier.padding(vertical = 4.dp), style = MaterialTheme.typography.bodyMedium)
            }
        }
    }
}

// Network Helpers
suspend fun fetchServerData(endpoint: String): JSONObject? = withContext(Dispatchers.IO) {
    try {
        val url = URL("$SERVER_URL$endpoint")
        val connection = url.openConnection() as HttpURLConnection
        JSONObject(connection.inputStream.bufferedReader().readText())
    } catch (e: Exception) { null }
}

suspend fun sendCommand(command: String) = withContext(Dispatchers.IO) {
    try {
        val url = URL("$SERVER_URL/api/command/$command")
        val connection = url.openConnection() as HttpURLConnection
        connection.requestMethod = "POST"
        connection.responseCode
    } catch (e: Exception) { }
}
