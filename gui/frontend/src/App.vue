<template>
  <div id="app">
      <el-row>
        <el-col :span="10">
          <div style="height:500px; border:1px solid black">
             <el-table
              :data="tableData"
              style="width: 100%"
              :highlight-current-row="true"
               @current-change="handleCurrentChange"
              max-height=500>
               <el-table-column
                prop="index"
                label="index"
                width="100">
              </el-table-column>
              <el-table-column
                prop="Year"
                label="Year"
                sortable
                width="100">
              </el-table-column>
              <el-table-column
                prop="Title"
                label="Title">
              </el-table-column>
              <el-table-column
                prop="AuthorNames"
                label="AuthorNames">
              </el-table-column>
             
            </el-table>
          </div>
        </el-col>
         <el-col :span="14">
          <div style="height:500px; border:1px solid black; border-left:0px solid white; overflow-y: scroll;">
            <div id="div_abstract">
              <el-button  v-for="item in wordList" :key="item.index" type="info" plain @click.native="clickWord(item.word)" size="small"  id="word_button">{{item.word}}</el-button>
            </div>
          </div>
         </el-col>
      </el-row>
      <el-row>
        <div style="height:500px; border:1px solid black">
          <el-row>
            <!-- <el-col :span="2"> -->
              <el-button type="danger" plain @click="clearKeyword">Clear</el-button>
            <!-- </el-col> -->
             <!-- <el-col :span="3"> -->
              <el-button  type="success" plain @click="manuSaveKeyword">Save</el-button>
            <!-- </el-col> -->
            
          </el-row>
          <el-tag
            v-for="tag in keyword"
            :key="tag"
            closable
            size="large"
            :disable-transitions="false"
            @close="removeKeyword(tag)"
            style="margin-left:5px; margin-bottom:5px">
            {{tag}}
          </el-tag>
        </div>
      </el-row>

  </div>
</template>

<script>
import River from './components/River.vue'
import axios from 'axios'
import * as d3 from 'd3'
export default {
  name: 'App',
  components:{
    River,
  },
  data(){
    return{
      tableData:[],
      currentRow:null,
      oldRow:null,
      wordList:null,
      keyword:[]
    }
  },
  created(){
    this.getTableData()
  },
  methods:{
    clearKeyword(){
      this.keyword = []
    },
    manuSaveKeyword(){
      const path = "http://localhost:5000/addKeyword"
      const payload={
        'DOI':this.currentRow['DOI'],
        'keyword':this.keyword
      }
      axios.post(path, payload)
      .then((res)=>{
        this.$message({
          message: 'Good job!',
          type: 'success'
        });
        // this.getTableData()
      })
      .catch((error)=>{
        console.log(error)
      })
    },
    saveKeyword(){
      console.log('save',this.currentRow['LabelKeyword']);
      const path = "http://localhost:5000/addKeyword"
      const payload={
        'DOI':this.oldRow['DOI'],
        'keyword':this.keyword
      }
      axios.post(path, payload)
      .then((res)=>{
        this.$message({
          message: 'Good job!',
          type: 'success'
        });
        // this.getTableData()
      })
      .catch((error)=>{
        console.log(error)
      })
    },
    removeKeyword(word){
       this.keyword.splice(this.keyword.indexOf(word), 1);
    },
    clickWord(val){
      this.keyword.push(val);
    },
    getTableData(){
      const path = "http://localhost:5000/getGraphData"
      axios.get(path)
      .then((res)=>{
        this.tableData = res.data.tableData
      })
      .catch((error)=>{
        console.log(error)
      })
    },
    getKeyword(){
      console.log('get keyword', this.currentRow['LabelKeyword'])
      const path = "http://localhost:5000/getKeyword"
      const payload = {
        'DOI': this.currentRow['DOI']
      }
      axios.post(path, payload)
      .then((res)=>{
        console.log(res.data)
        this.keyword = res.data.keyword
        // this.tableData = res.data.tableData
      })
      .catch((error)=>{
        console.log(error)
      })
    },
    handleCurrentChange(val,old) {
      if(old===null){
        this.oldRow = val
        this.currentRow = val
      }else{
        this.currentRow = val;
        this.oldRow = old;
      }
      //save data
      this.saveKeyword()
      this.getKeyword()
    },
    changeAbstract(){
       var temp_list = this.currentRow['Abstract'].split(' ')
       var hasIndex = []
       for(let i=0; i<temp_list.length;i++){
         hasIndex.push({
           'index':i,
           'word':temp_list[i]
         })
       }
      this.wordList = hasIndex;
    }

  },
  watch:{
    currentRow(){
      this.changeAbstract()
    }
  },
  mounted(){

  },
  computed:{

  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.el-tag{
  font-size:17px;
}
.el-button+.el-button {
    margin-left: 0px;
}
.el-button--info.is-plain:hover {
    /* background: #909399; */
    border-color: #909399;
    color: black;
}
.el-button--info.is-plain:focus {
    /* background: #909399; */
    border-color: red;
    color: black;
}
.el-button--info.is-plain {
    color: #909399;
    background: white;
    border-color: white;
}
.el-button--mini, .el-button--small {
    font-size: 17px;
    border-radius: 3px;
}
.el-button--small, .el-button--small.is-round {
    padding: 8px 4px;
}
.el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
</style>
