package io.github.danielseisenbacher.predictable

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.runtime.getValue
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import io.github.danielseisenbacher.predictable.data.AppViewModel
import io.github.danielseisenbacher.predictable.ui.App
import io.github.danielseisenbacher.predictable.ui.theme.PredictableTheme

class MainActivity : ComponentActivity() {
    private val vm: AppViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        enableEdgeToEdge()
        super.onCreate(savedInstanceState)
        setContent {
            val dynamic by vm.dynamicColor.collectAsStateWithLifecycle()
            PredictableTheme(dynamicColor = dynamic) {
                App(vm)
            }
        }
    }
}
