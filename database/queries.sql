select sum(r.resposta) as 'Performance no Desempenho'
from respostas r
join perguntas p on p.id=r.pergunta_id
join competencias c on c.id=p.competencia_id
where c.tipo_performance='Desempenho'
  and r.formulario_id=38;

select sum(r.resposta) as 'Performance no Engajamento'
from respostas r
join perguntas p on p.id=r.pergunta_id
join competencias c on c.id=p.competencia_id
where c.tipo_performance='Engajamento'
  and r.formulario_id=38;

select sum(r.resposta) as 'Performance na Organização'
from respostas r
join perguntas p on p.id=r.pergunta_id
join competencias c on c.id=p.competencia_id
where c.tipo_performance='Organização'
  and r.formulario_id=38;

select sum(r.resposta) / count(c.id) as media_grupo, c.grupo_id
from respostas r
join perguntas p on p.id=r.pergunta_id
join competencias c on c.id=p.competencia_id
where c.tipo_impacto='Gestão'
  and r.formulario_id=38
group by c.grupo_id;

select sum(r.resposta) / count(c.id) as media_grupo, c.grupo_id
from respostas r
join perguntas p on p.id=r.pergunta_id
join competencias c on c.id=p.competencia_id
where c.tipo_impacto='Equipes'
  and r.formulario_id=38
group by c.grupo_id;