<template>
  <div ref="rootEl" style="height: 150px; width: 100%" class="ag-theme-alpine">
  </div>
</template>

<script lang="ts">

import 'ag-grid-community/styles//ag-grid.css';
import 'ag-grid-community/styles//ag-theme-alpine.css';

const defaultSpec = {
  columnDefs: [
    {headerName: 'Make', field: 'make'},
    {headerName: 'Model', field: 'model'},
    {headerName: 'Price', field: 'price'}
  ],
  rowData: [
    {make: 'Toyota', model: 'Celica', price: 35000},
    {make: 'Ford', model: 'Mondeo', price: 32000},
    {make: 'Porsche', model: 'Boxster', price: 7200}
  ]
};

import {FieldType} from "../streamsyncTypes";
export default {

  streamsync: {
    name: "Ag Grid",
    description: "",
    category: "Content",

    // Fields will be editable via Streamsync Builder

    fields: {
      spec: {
        name: "Grid specification",
        default: JSON.stringify(defaultSpec, null, 2),
        desc: "Ag Grid specification",
        type: FieldType.Object,
      },
    },
  },
};

</script>
<script setup lang="ts">
import { inject, onMounted, ref, Ref, watch} from "vue";
import injectionKeys from "../injectionKeys";


/*
The values for the fields defined earlier in the custom option
will be available using the evaluatedFields injection symbol.
*/


const rootEl: Ref<HTMLElement> = ref(null);
const fields = inject(injectionKeys.evaluatedFields);
let aggrid: any = null;

const renderGrid = async () => {
  if (import.meta.env.SSR) return;
  if (!fields.spec.value || !rootEl.value) return;
  const {Grid} = await import('ag-grid-community');
  if (aggrid === null) {
    aggrid = new Grid(rootEl.value, fields.spec.value);
  } else {
    aggrid.gridOptions.api.setRowData(fields.spec.value.rowData);
  }
};

watch(() => fields.spec.value, (spec) => {
	if (!spec) return;
	renderGrid();
});

onMounted(() => {
  renderGrid();
  if (!rootEl.value) return;
  // new ResizeObserver(renderGrid).observe(rootEl.value, {
  //   box: "border-box",
  // });
});

</script>

<style scoped>
</style>