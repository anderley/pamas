// Call the dataTables jQuery plugin
$(document).ready(function() {
  $('#dataTable').DataTable({
    ordering: false,
    searching: false,
    lengthChange: false,
    language: {
        info: 'Exibindo _START_ a _END_ do total de _TOTAL_',
        paginate: {
            first: 'Primeira',
            previous: 'Anterior',
            next: 'Próxima',
            last: 'Última'
        },
    }
  });
});
