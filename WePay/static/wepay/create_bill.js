Vue.component('charttitle',{
    data() {
      return { 
        message: 'Create Bills',
        collapsed: true
      }
    },
    template:`
  <div id ="chart_title">
      <label>
      <input v-model="message" placeholder="Insert the chart title" v-bind:class="[ {'is-collapsed' : collapsed }, 'inputHide' ]" type="text">
      </label>
      <h2>{{ message }} <button class="hideshow" v-on:click=" collapsed = !collapsed"><i class="fa fa-pencil" aria-hidden="true"></i></button></h2>
    </div>
  `
  })
  
  /* Second header */
  
  Vue.component('chartsubtitle',{
    data() {
      return { 
        message: 'Data reports',
        collapsed: true
      }
    },
    template:`
  <div id ="chart_subtitle">
      <label>
      <input v-model="message" placeholder="Insert the chart title" v-bind:class="[ {'is-collapsed' : collapsed }, 'inputHide' ]" type="text">
      </label>
      <h2>{{ message }} <button class="hideshow" v-on:click=" collapsed = !collapsed"><i class="fa fa-pencil" aria-hidden="true"></i></button></h2>
    </div>
  `
  })
  
  
  Vue.component('charttable',{
    props:['proplabels'],
    data() {
      return{
      disabled: true
      }
    },
    methods:{
      deleteEvent: function(index) {
        this.proplabels.splice(index, 1);
      }
  },
    template:
      `
  <div id="chart_table">
          <div class="top_titles">
              <div class="small-12 medium-1 column"> No. </div>
              <div class="small-12 medium-2 column"> title </div>
              <div class="small-12 medium-4 column"> Bills </div>
              <div class="small-12 medium-2 column"> Price </div>
              <div class="small-12 medium-2 column"> Assign </div>
              <div class="small-12 medium-1 column"> Edit
                  <i class="fa fa-trash" aria-hidden="true"></i>
              </div>
          </div>
          
      <div v-for="(val, index)al in proplabels" class="row table_cell">
          <div class="small-12 medium-1 column">
              <input type="text" v-model="val.id" disabled></input>
          </div>
          <div  class="small-12 medium-2 column single-cel">
              <input type="text" v-model="val.title" v-bind:disabled="disabled">
              </input>
          </div>
          <div class="small-12 medium-4 column single-cel">
              <input type="text" v-model="val.label" v-bind:disabled="disabled"> </input>
          </div>
          <div class="small-12 medium-2 column single-cel">
              <input type="text" v-model="val.price" v-bind:disabled="disabled"> </input>
          </div>
          <div class="small-12 medium-2 column single-cel">
              <input type="text" v-model="val.assign" v-bind:disabled="disabled"> </input>
          </div>
          <div class="small-12 medium-1 column edit_panel">
              <button @click="deleteEvent(index)">
                  <i class="fa fa-times" aria-hidden="true"></i>
              </button>
  <span class="edit_mode" @click="disabled = !disabled">
                  <i class="fa fa-pencil-square-o" aria-hidden="true"></i>
              </span>
          </div>
      </div>
  
  
  </div>
  
  `
  })
  
  
  new Vue({
          el: '#chartpanel',
          data: {
              value: '',
              label: '',
              price: '',
              assign:'',
            labels: [ { id:0, title: 87, label:'Mandorle', assign:'fa-user-circle-o' } ],
            nextBarId: 1
          },
          computed: {
              
          },
          methods: {
              addRow: function (event) {
                lastId =  this.labels.length;
                var newRow={
                  id: this.nextBarId++, 
                  title: this.value, 
                  label: this.label , 
                  assign: this.assign
                };
                this.labels.push( newRow );
              }
            
          }
      });
  
  
  
  
  
  
  