
function PonyHelper_send_to(where, text){
    textarea = gradioApp().querySelector('#PonyHelper_selected_text textarea')
    textarea.value = text
    updateInput(textarea)

    gradioApp().querySelector('#PonyHelper_send_to_'+where).click()

    where == 'txt2img' ? switch_to_txt2img() : switch_to_img2img()
}

function PonyHelper_send_to_txt2img(text){ PonyHelper_send_to('txt2img', text) }
function PonyHelper_send_to_img2img(text){ PonyHelper_send_to('img2img', text) }

function submit_PonyHelper(){
    var id = randomId()
    requestProgress(id, gradioApp().getElementById('PonyHelper_results_column'), null, function(){})

    var res = create_submit_args(arguments)
    res[0] = id
    return res
}
    // Function to format tags without category names and unnecessary symbols
    function formatTags(tagsResult) {
        var formattedTags = '';
        for (var key in tagsResult) {
            if (tagsResult.hasOwnProperty(key)) {
                formattedTags += tagsResult[key].replace(/"|:/g, '') + ', ';
            }
        }
        // Remove the trailing comma and space
        formattedTags = formattedTags.slice(0, -2);
        return formattedTags;
    }
		
$(document).ready(function(){
    $("#generate-tags-button").click(function(e){
    e.preventDefault();
    $.ajax({
        url: '/generate-tags/' + $('#category').val(),  // Include the selected category in the URL
        type: 'POST',
        data: $('form').serialize(),
        success: function(response){
            // Update the tags box with the generated tags
            $('.tags-box p').text(response.tags_result);
        },
        error: function(error){
            console.log(error);
        }
    });

        // Fetch updated CFG scale and sampling steps
        fetch('/generate-random-values')
            .then(response => response.json())
            .then(data => {
                // Update the CFG scale and sampling steps elements in the HTML
                $('#cfg-scale').text("CFG Scale: " + data.cfg);
                $('#sampling-steps').text("Sampling Steps: " + data.steps);
            })
            .catch(error => console.error('Error:', error));
    });
});
    // JavaScript function to handle the response and update the character tags box
    document.addEventListener('DOMContentLoaded', function() {
        const charactersForm = document.getElementById('characters-form');
        const charactersTagsBox = document.getElementById('characters-tags-box');
        const generateCharacterButton = document.getElementById('generate-character-button');

        generateCharacterButton.addEventListener('click', function() {
            fetch(charactersForm.getAttribute('action'), {
                method: 'POST',
                body: new FormData(charactersForm)
            })
            .then(response => response.json())
            .then(data => {
                charactersTagsBox.innerHTML = ''; // Clear existing content
                const p = document.createElement('p');
                p.textContent = data.characters_result; // Set text content to the generated character tags
                charactersTagsBox.appendChild(p); // Append the <p> element to the character tags box
            })
            .catch(error => console.error('Error:', error));
        });

        // Prevent default form submission
        charactersForm.addEventListener('submit', function(event) {
            event.preventDefault();
        });
    });

	// Function to handle form submission and display generated tags
function handleFormSubmit(form, resultElement) {
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        // Send a POST request to the form's action URL
        fetch(form.action, {
            method: 'POST',
            body: new FormData(form)
        })
        .then(response => response.json())
        .then(data => {
            // Update the result element with the generated tags
            resultElement.textContent = data.result || data.characters_result;
        })
        .catch(error => console.error('Error:', error));
    });
}

  function handleButtonClick(type) {
    const generatedPrompt = "Your generated prompt goes here"; // Replace with actual prompt

    if (type === "img2img") {
      Ponyhelper_send_to_img2img(generatedPrompt);
    } else if (type === "txt2img") {
      Ponyhelper_send_to_txt2img(generatedPrompt);
    }
  }

  // Event listeners for button clicks
  document.getElementById("img2imgButton").addEventListener("click", () => {
    handleButtonClick("img2img");
  });

  document.getElementById("txt2imgButton").addEventListener("click", () => {
    handleButtonClick("txt2img");
  });
	
// Get the forms and result elements
const tagsForm = document.getElementById('tags-form');
const charactersForm = document.getElementById('characters-form');
const tagsResult = document.getElementById('tags-result');
const charactersResult = document.getElementById('characters-result');

// Handle form submission for generating DanBooru tags
handleFormSubmit(tagsForm, tagsResult);

// Handle form submission for generating character tags
handleFormSubmit(charactersForm, charactersResult);
		
        // Add JavaScript code to validate the form input
        document.addEventListener('DOMContentLoaded', function() {
            const form = document.querySelector('form');

            form.addEventListener('submit', function(event) {
                const numWordsInput = document.getElementById('num_words');
                const numWords = parseInt(numWordsInput.value);

                if (isNaN(numWords) || numWords < 1 || numWords > 50) {
                    alert('Please enter a valid number of DanBooru tags (1-50).');
                    event.preventDefault(); // Prevent form submission
                }
            });
        });
    });
