/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
const getList = async () => {
  let url = 'http://127.0.0.1:5000/casas';
  fetch(url, {
    method: 'get',
  })
    .then((response) => response.json())
    .then((data) => {
      data.casas.forEach(item => insertList(item.address,
                                          item.square_feet,
                                          item.bedrooms,
                                          item.bathrooms,
                                          item.neighborhood,
                                          item.year_built,
                                          item.price_range
                                        ))
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para limpar a tabela antes de recarregar os dados
  --------------------------------------------------------------------------------------
*/
const clearTable = () => {
  var table = document.getElementById('myTable');
  // Remove todas as linhas exceto o cabeçalho (primeira linha)
  while(table.rows.length > 1) {
    table.deleteRow(1);
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para recarregar a lista completa do servidor
  --------------------------------------------------------------------------------------
*/
const refreshList = async () => {
  clearTable();
  await getList();
}

/*
  --------------------------------------------------------------------------------------
  Chamada da função para carregamento inicial dos dados
  --------------------------------------------------------------------------------------
*/
// Carrega a lista apenas uma vez quando a página é carregada
document.addEventListener('DOMContentLoaded', function() {
  getList();
});




/*
  --------------------------------------------------------------------------------------
  Função para colocar um item na lista do servidor via requisição POST
  --------------------------------------------------------------------------------------
*/
const postItem = async (inputAddress, inputSquareFeet, inputBedrooms,
                        inputBathrooms, inputNeighborhood, 
                        inputYearBuilt) => {
    
  const formData = new FormData();
  formData.append('address', inputAddress);
  formData.append('square_feet', inputSquareFeet);
  formData.append('bedrooms', inputBedrooms);
  formData.append('bathrooms', inputBathrooms);
  formData.append('neighborhood', inputNeighborhood);
  formData.append('year_built', inputYearBuilt);

  let url = 'http://127.0.0.1:5000/casa';
  return fetch(url, {
    method: 'post',
    body: formData
  })
    .then((response) => response.json())
    .then((data) => {
      return data; // Retorna os dados da casa com a previsão de preço
    })
    .catch((error) => {
      console.error('Error:', error);
      throw error;
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para criar um botão close para cada item da lista
  --------------------------------------------------------------------------------------
*/
const insertDeleteButton = (parent) => {
  let span = document.createElement("span");
  let txt = document.createTextNode("\u00D7");
  span.className = "close";
  span.appendChild(txt);
  parent.appendChild(span);
}

/*
  --------------------------------------------------------------------------------------
  Função para remover um item da lista de acordo com o click no botão close
  --------------------------------------------------------------------------------------
*/
const removeElement = () => {
  let close = document.getElementsByClassName("close");
  // var table = document.getElementById('myTable');
  let i;
  for (i = 0; i < close.length; i++) {
    close[i].onclick = function () {
      let div = this.parentElement.parentElement;
      const enderecoItem = div.getElementsByTagName('td')[0].innerHTML
      if (confirm("Você tem certeza?")) {
        div.remove()
        deleteItem(enderecoItem)
        alert("Removido!")
      }
    }
  }
}

/*
  --------------------------------------------------------------------------------------
  Função para deletar um item da lista do servidor via requisição DELETE
  --------------------------------------------------------------------------------------
*/
const deleteItem = (item) => {
  console.log(item)
  let url = 'http://127.0.0.1:5000/casa?address='+item;
  fetch(url, {
    method: 'delete'
  })
    .then((response) => response.json())
    .catch((error) => {
      console.error('Error:', error);
    });
}

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item com nome, quantidade e valor 
  --------------------------------------------------------------------------------------
*/
const newItem = async (event) => {
  event.preventDefault();

  let inputAddress = document.getElementById("newAddress").value;
  let inputSquareFeet = document.getElementById("newSquareFeet").value;
  let inputBedrooms = document.getElementById("newBedrooms").value;
  let inputBathrooms = document.getElementById("newBathrooms").value;
  let inputNeighborhood = document.getElementById("newNeighborhood").value;
  let inputYearBuilt = document.getElementById("newYearBuilt").value;

  // Verifique se o endereço da casa já existe antes de adicionar
  const checkUrl = `http://127.0.0.1:5000/casas?address=${inputAddress}`;
  fetch(checkUrl, {
    method: 'get'
  })
    .then((response) => response.json())
    .then(async (data) => {
      if (data.casas && data.casas.some(item => item.address === inputAddress)) {
        alert("A casa com este endereço já está cadastrada.\nCadastre a casa com um endereço diferente.");
      } else if (inputAddress === '') {
        alert("O endereço da casa não pode ser vazio!");
      } else if (isNaN(inputSquareFeet) || isNaN(inputBedrooms) || isNaN(inputBathrooms) || isNaN(inputNeighborhood) || isNaN(inputYearBuilt)) {
        alert("Esses campos precisam ser números!");
      } else {
        try {
          // Envia os dados para o servidor e aguarda a resposta com a predição de preço
          const result = await postItem(inputAddress, inputSquareFeet, inputBedrooms, inputBathrooms, inputNeighborhood, inputYearBuilt);
            // Limpa o formulário
          document.getElementById("newAddress").value = "";
          document.getElementById("newSquareFeet").value = "";
          document.getElementById("newBedrooms").value = "";
          document.getElementById("newBathrooms").value = "";
          document.getElementById("newNeighborhood").value = "";
          document.getElementById("newYearBuilt").value = "";
          
          // Recarrega a lista completa para mostrar a nova casa com a predição
          await refreshList();
          
          // Mostra mensagem de sucesso com a faixa de preço
          const priceRange = result.price_range;
          alert(`Casa adicionada com sucesso!\nFaixa de preço: ${priceRange}`);
          
          // Scroll para a tabela para mostrar o novo resultado
          document.querySelector('.items').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
          });
          
        } catch (error) {
          console.error('Erro ao adicionar casa:', error);
          alert("Erro ao adicionar casa. Tente novamente.");
        }
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      alert("Erro ao verificar casa existente. Tente novamente.");
    });
}


/*
  --------------------------------------------------------------------------------------
  Função para inserir items na lista apresentada
  --------------------------------------------------------------------------------------
*/
const insertList = (address, squareFeet, bedrooms, bathrooms, neighborhood, yearBuilt, priceRange) => {
  var item = [address, squareFeet, bedrooms, bathrooms, neighborhood, yearBuilt];
  var table = document.getElementById('myTable');
  var row = table.insertRow();

  // Insere as células com os dados da casa
  for (var i = 0; i < item.length; i++) {
    var cell = row.insertCell(i);
    cell.textContent = item[i];
  }

  // Insere a célula da faixa de preço com styling
  var priceCell = row.insertCell(item.length);
  priceCell.textContent = priceRange;
  
  // Aplica styling baseado na faixa de preço
  if (priceRange <= 3) {
    priceCell.className = "price-low";
  } else if (priceRange <= 6) {
    priceCell.className = "price-medium";
  } else {
    priceCell.className = "price-high";
  }

  // Insere o botão de deletar
  var deleteCell = row.insertCell(-1);
  insertDeleteButton(deleteCell);

  removeElement();
}