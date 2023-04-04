<!DOCTYPE html>
<html>
<head>
  <title>My Web Application</title>
  <script src="https://cdn.jsdelivr.net/npm/vue/dist/vue.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
</head>
<body>
  <div id="app">
    <form id="myForm">
      <!-- input fields go here -->
      <input type="file" name="file" ref="fileInput">
      <button @click.prevent="submitForm">Predict</button>
    </form>
    <div v-if="prediction">
      <!-- display the prediction results here -->
      <h3>Prediction:</h3>      
      <a :href="csvUrl" download="predictions.csv">Download CSV</a>
      <ul>
        <li v-for="p in prediction" :key="p" v-text="p"></li>
      </ul>
    </div>
  </div>
  <script src="{{ url_for('static', filename='js/vue.js') }}"></script>
  <script>
    var app = new Vue({
      el: '#app',
      data: {
        prediction: "",
        csvUrl: ""
      },
      methods: {
        submitForm: function() {
          var formData = new FormData();
          formData.append('file', this.$refs.fileInput.files[0]);

          axios.post('/post/', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
              'X-Requested-With': 'XMLHttpRequest'
            },
            responseType: 'blob'
          })
          .then(function(response) {
            // check the response before creating the Vue component
            if (response.status === 200) {
              console.log(response.data);
              // parse response data if content type is json
              var contentType = response.headers['content-type'];
              if (contentType.indexOf('application/json') !== -1) {
                app.prediction = response.data.Prediction;
              } else {
                var reader = new FileReader();
                reader.onload = function() {
                  app.prediction = reader.result.split("\n").filter(Boolean);
                }
                reader.readAsText(response.data);
                app.csvUrl = URL.createObjectURL(new Blob([response.data], {type: 'text/csv'}));
              }
            } else {
              console.log('An error occurred.');
            }
          })
          .catch(function(error) {
            console.log(error);
          });
        }
      },
      delimiters: ['[[', ']]']
    });
  </script>
</body>
</html>
