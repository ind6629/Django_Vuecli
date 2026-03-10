//import * as echarts from 'echarts';
//import * as echarts from 'https://cdn.jsdelivr.net/npm/echarts@5.4.3/+esm';
  
function clickTable(){
  var chartDom = document.querySelector('.showBox');
  var myChart = echarts.init(chartDom);
  var option;

  datax = [];
  datay = [];
  products.forEach(product => {
    datax.push(`${product.category}`);
    datay.push(`${product.times}`);
    });
  console.log(datax,datay);

option = {
  xAxis: {
    type: 'category',
    data: datax,
    axisLabel: {
      interval: 0,// 强制显示
      rotate: 30,//旋转30°
    }
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: datay,
      type: 'bar'
    }
  ]
};
option && myChart.setOption(option);
console.log('加载')
}

document.addEventListener('DOMContentLoaded', function() {
  clickTable();
});