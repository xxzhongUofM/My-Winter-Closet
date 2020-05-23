var minPrice = 0
var maxPrice = 500

var currentMin = minPrice
var currentMax = maxPrice

var resultView = new Vue({
	el: '#app',
  	data: {
        master_items: [],
    	filtered_items: [],
    	categories: [],
        button_status: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        departments: [],
        num_results: 0,
 	},
    mounted () {
        axios
          .get('static/clothes.json')
          .then(response => (this.master_items = response.data, this.filterItems()))
    },
  	methods: {
        filterItems: function(){
            this.filtered_items = [];
            // dept -> category -> price
            if(this.departments.length != 0){
                for (var i = 0; i < this.master_items.length; i++) {
                    let dept = this.master_items[i]["department"]
                    if (this.departments.includes(dept)) {
                        this.filtered_items.push(this.master_items[i]);
                    }
                }
            }
            else{
                this.filtered_items = this.master_items;
            }
            //category
            if(this.categories.length != 0){
                var temp = [];
                for(var i = 0; i < this.filtered_items.length; i++){
                    let type = this.filtered_items[i]["product_type"];
                    if (this.categories.includes(type)) {
                        temp.push(this.filtered_items[i]);
                    }
                }
                this.filtered_items = temp;
            }

            var temp2 = [];
            for(var i = 0; i < this.filtered_items.length; i++){
                let price = this.filtered_items[i]["sale_price"]
                if(currentMin <= price && price <= currentMax) {
                    temp2.push(this.filtered_items[i]);
                }
            }
            this.filtered_items = temp2;

            //true: low to high
            if(this.button_status[11]){
                this.sortLowToHigh();
            }
            else{
                this.sortHighToLow();
            }
            resultView.filtered_items.splice(this.filtered_items.length);
        },
  		addRemoveCategory: function (category, index) {      
            // Add or remove category from list.
            if (!this.categories.includes(category)) {
                this.categories.push(category)
                this.$set(this.button_status, index, 1)
            } else {
                let cat_idx = this.categories.indexOf(category)
                this.categories.splice(cat_idx, 1)
                this.$set(this.button_status, index, 0)
            }
            this.filterItems();
            
        },
        addRemoveDepartment: function (department, index) {
              // Add or remove department from list.
              if (!this.departments.includes(department)) {
                this.departments.push(department)
                this.$set(this.button_status, index, 1)
            } else {
                let cat_idx = this.departments.indexOf(department)
                this.departments.splice(cat_idx, 1)
                this.$set(this.button_status, index, 0)
            }

            this.filterItems();
        },
        sortLowToHigh: function () {
            this.filtered_items.sort(function(first, second) {return first.sale_price - second.sale_price;});
            resultView.filtered_items.splice(this.filtered_items.length);
        },
        sortHighToLow: function () {
            this.filtered_items.sort(function(first, second) {return second.sale_price - first.sale_price;});
            resultView.filtered_items.splice(this.filtered_items.length);
        },
        togglePriceSorting: function(){
            this.$set(this.button_status, 11, !this.button_status[11]);
            this.filterItems();
        }
  	}
})

$(document).ready(function () {
  $('#slider-container').slider({
      range: true,
      min: minPrice,
      max: maxPrice,
      values: [minPrice, maxPrice],
      create: function() {
          $("#amount").val("$" + minPrice + " - $" + maxPrice);
      },
      slide: function (event, ui) {
          $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
          var mi = ui.values[0];
          var mx = ui.values[1];
          currentMin = ui.values[0]
          currentMax = ui.values[1]
          resultView.filterItems();
          console.log(resultView.filtered_items)
          filterSystem(mi, mx);
      }
  })
});

function filterSystem(minPrice, maxPrice) {
    $("#computers div.system").hide().filter(function () {
        var price = parseInt($(this).data("price"), 10);
        return price >= minPrice && price <= maxPrice;
    }).show();
}
