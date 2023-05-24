<template>
  <div id="main">
    <div v-if="!is_telegram_client" class="text-center">
      Please open the app from a Telegram client!<br>
    </div>
    <div v-if="is_telegram_client && !is_telegram_api_updated" class="text-center">
      Please update Telegram to Use the app!<br>
      Telegram API version needed 6.4 or greater.<br>
      Your Telegram API version: {{ TWA.version }}
    </div>
  </div>
</template>

<script>
import { prepareUrl } from './helpers'

export default {
  data() {
    return {
      is_telegram_client: false,
      is_telegram_api_updated: false,
      code: null,
      is_url: false,
      url: null,
    };
  },
  created() {
    // Binding function to all the event types
    // this.TWA.onEvent('themeChanged', this.themeChanged);
    this.TWA.MainButton.setText("Scan QR");     // LOCALE
    this.TWA.onEvent('qrTextReceived', this.processQRCode);
    this.TWA.onEvent('mainButtonClicked', this.mainButtonClicked);

    this.is_telegram_api_updated = this.TWA.isVersionAtLeast('6.4');
    // platform not updated if version is not 6.4 or greater

    if (this.TWA.platform != "unknown") {
      this.is_telegram_client = true;
    }

    if (this.is_telegram_client && this.is_telegram_api_updated) {
      this.TWA.MainButton.show();
      this.showQRScanner();
    }
  },
  mounted() {
    this.TWA.ready();
  },
  methods: {
    // attached with onEvent function during created
    // themeChanged() {
    //   this.TWA.showAlert('Theme has changed');
    // },
    mainButtonClicked() {
       this.showQRScanner();
    },
    processQRCode(data) {
       this.code = data.data;
       const result = prepareUrl(this.code)
       this.is_url = result.is_url;
       this.url = result.value;
       this.hapticImpact();
       this.TWA.closeScanQrPopup();
       navigator.clipboard.writeText(result.value).then(
            () => {this.TWA.showAlert('Text copied to clipboard', () => {this.TWA.close()});},
            () => {this.TWA.close()}
       );
    },
    // End of callbacks
    showQRScanner() {
      const par = {
          text: ""
        };
      this.TWA.showScanQrPopup(par);
    },
    hapticImpact() {
      // light medium heavy rigid soft
      this.TWA.HapticFeedback.impactOccurred("heavy");
    }
  }
}
</script>

<style scoped>
#main {
  background-color: var(--tg-theme-bg-color, white);
  color: var(--tg-theme-text-color, black);
  /*https://stackoverflow.com/questions/1165497/how-to-prevent-text-from-overflowing-in-css*/
  word-wrap: break-word;
}
b {
  color: var(--tg-theme-hint-color, black);
}
h3 {
  color: var(--tg-theme-text-color, black);
}
button {
  background-color: var(--tg-theme-button-color, #008CBA);
  border: 5px;
  color: var(--tg-theme-button-text-color, black);
  padding: 15px;
  margin: 5px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 15px;
}
</style>
