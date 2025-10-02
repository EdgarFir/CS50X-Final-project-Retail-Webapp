document.addEventListener('DOMContentLoaded', async function () {
    // Adjust elements
    adjustElements();
    
    // Add event listener to close pop-over buttons
    closePopOverButton();

    // Allow tooltips
    allowToolTips();

    // Adjust elements when page is resized 
    window.addEventListener('resize', adjustElements);

    // Ensure that javascript is used in right template
    if (document.title == 'Index') {

        if (document.getElementById('index_main_content')) {
            await requestIndexMainInfo();
        }
        else {
            document.querySelector('main').style.minHeight = '610px';
        }       
    }
    else if (document.title == 'Set personal code' || document.title == 'Recover password') {
        // Handle personal code input
        handlePersonalCodeInput();
    }
    else if (document.title == 'Settings') {
        // Add click event listener to change company name link
        document.getElementById('change_company_name').addEventListener('click', requestChangeCompanyNameForm);
        
        // Add click event listener to change currency link
        document.getElementById('change_currency').addEventListener('click', requestChangeCurrencyForm);

        // Add event listener to links and buttons with authenticator class
        document.querySelectorAll('.authenticator').forEach(authenticator_element => {
            authenticator_element.addEventListener('click', async function(event) {
                // Prevent window reload
                event.preventDefault();

                // Request authenticator options form
                await requestAuthenticatorOptions(authenticator_element.id);
            })
        })
    }
    else if (document.title == 'Products and services') {

        // Products and system navbar links 
        const vertical_nav_bar_buttons = document.querySelectorAll('.main-button');
        
        // Add event listeners to main, sub and show data buttons to change active and sub active classes between respective buttons
        vertical_nav_bar_buttons.forEach(button => {
            button.addEventListener('click', changeActiveMainButton);
         });

        // My products and services nav bar link
        const products_and_services_link = document.getElementById('my_products_and_services');

        // Add event listener to my products and services nav bar link
        products_and_services_link.addEventListener('click', requestMyProductsAndServicesHtml);

        simulateClickEvent(products_and_services_link);

        // Register products link
        const register_products_link = document.getElementById('register_products');

        // Add event listener to register products link
        register_products_link.addEventListener('click', requestRegisterProductsForm);

        // Register services link
        const register_services_link = document.getElementById('register_services');

        // Add event listener to register services link
        register_services_link.addEventListener('click', requestRegisterServicesForm);

        // Edit products and services link
        const edit_products_and_services_link = document.getElementById('edit_products_and_services');

        // Add event listener to edit products and services link
        edit_products_and_services_link.addEventListener('click', requestEditProductsAndServicesHtml);
    }
    
    // Ensure that javascript is used in right template
    else if (document.title == 'Register orders') {

         // Description input
         const description_input = document.getElementById('description');

         // Add event listener to description input
         description_input.addEventListener('input', async function(event) {
             await requestProductOrServiceAutoComplete(event, 'order_product');
         });

        // Submit product to order button
        const submit_product_to_order_list_button = document.getElementById('submit_product_to_order_list')

        // Delete all products from order button
        const delete_all_products_from_order_button = document.getElementById('delete_products_from_order');
        
        // Upload input
        const upload_order_input = document.getElementById('upload_order');

        // Register order button
        const register_order_button = document.getElementById('register_order');

        // Add event listener to submit products to order list button
        submit_product_to_order_list_button.addEventListener('click', async function(event) {
            // Prevent window reload
            event.preventDefault();

            if (sessionStorage.getItem('order_product')) {
                // Get product id storaged in sessionStorage
                const product_id = sessionStorage.getItem('order_product');

                // Send product data to validate and insert in temp order list
                await sendProductToValidateAndInsertinTempOrderList(event, product_id);
            }

        });

        // Add event listener to register_order button
        register_order_button.addEventListener('click', registerOrder);

        // Add event listener to delete all products from order button
        delete_all_products_from_order_button.addEventListener('click', removeAllProductsFromOrderList);

        // Add event listener to upload order button
        upload_order_input.addEventListener('input', sendUploadedOrderAndValidate);

        // Request order table updated
        await requestOrderTableAndUpdate(0);
    
    }
    else if (document.title == 'Stocks manager') {
        // Clean session Storage search_product_id and search_service_id 
        cleanSessionStorage('search_product_id');
        cleanSessionStorage('search_service_id');



        // Select action select element
        const select_action = document.getElementById('stock_actions');

        // Product description or bar code to search input element
        const search_for_product_input = document.getElementById('description_bar_code');

        // Add event listener to search for product input
        search_for_product_input.addEventListener('input', function(event) {
            requestProductOrServiceAutoComplete(event, 'product'); 
        })

        // Service description or bar code to search input element
        const search_for_service_input = document.getElementById('service_description_bar_code');

          // Add event listener to search for service input
          search_for_service_input.addEventListener('input', function(event) {
            requestProductOrServiceAutoComplete(event, 'service');
        })

        // Select product or service div element
        const select_product_or_service_element = document.getElementById('select_product_or_service'); 
        
        // Search options select element
        const select_options_element = document.getElementById('search_options');

        // Search for product or service div element
        const search_product_or_service_element = document.getElementById('search_for_product_or_service');

        // Add event listener to select action element
        select_action.addEventListener('input', function (event) {

            // Clean sessionStorage if user restart the form
            cleanSessionStorage('search_product_id');
            cleanSessionStorage('search_service_id');

            // Search options
            const search_options = document.getElementsByName('search_actions_options');

            // Clean inputs
            search_for_product_input.value = '';
            search_for_service_input.value = '';

            search_options[0].selected = true;

            // Option value
            option_value = event.target.value;

            // Ensure which option is select
            if (option_value == 'register_waste' || option_value === 'consult_movements') {
                // Remove 'display-none' class from select product or service div element
                select_product_or_service_element.classList.remove('display-none');

                // Add 'display-none' class from search for product or service
                search_product_or_service_element.classList.add('display-none');

                // Add'display-none' class from search for product input
                search_for_product_input.classList.add('display-none');

                // Add event listener to search options select element
                select_options_element.addEventListener('input', function(event) {
                    // Remove 'display-none' class from search for product or service
                    search_product_or_service_element.classList.remove('display-none');

                    // Option value
                    const search_option_value = event.target.value;

                    // Ensure which option value to search is selected
                    if (search_option_value == 'product') {
                        // Remove 'display-none' class from search for product input
                        search_for_product_input.classList.remove('display-none');

                        // Add 'display-none' class from search for service input
                        search_for_service_input.classList.add('display-none');
                        
                        // Clean sessionStorage
                        cleanSessionStorage('search_service_id');

                        search_for_service_input.value = '';
                    }
                    else if (search_option_value == 'service') {
                        // Remove 'display-none' class from search for service input
                        search_for_service_input.classList.remove('display-none');

                        // Add'display-none' class from search for product input
                        search_for_product_input.classList.add('display-none');

                        // Clean sessionStorage
                        cleanSessionStorage('search_product_id');

                        search_for_product_input.value = '';
                    }
                })
            }
            else if (option_value === 'register_regularization') {
                // Add 'display-none' class from select product or service div element
                select_product_or_service_element.classList.add('display-none');

                // Remove 'display-none' class from search for product or service
                search_product_or_service_element.classList.remove('display-none');

                // Add 'display-none' class from search for service input
                search_for_service_input.classList.add('display-none');

                // Remove 'display-none' class from search for product input
                search_for_product_input.classList.remove('display-none');
            }
        })

        // Button to get stocks content
        get_stocks_content_button = document.getElementById('get_stocks_content');

        // Add event listener to get_stock_content_button
        get_stocks_content_button.addEventListener('click', async function(event) {
            // Prevent window reload
            event.preventDefault();

            // Ensure a product or service is selected
            if (sessionStorage.getItem('search_product_id') == null && sessionStorage.getItem('search_service_id') == null) {
                sendErrorMessage(event, 'Please select product or service!')
                throw new Error('Error status: 400, Error: Please select product or service!');
            }
            else if (sessionStorage.getItem('search_product_id') != null ) {
                // Request products stocks content 
                await requestStocksContent(event, 'product');

                console.log(sessionStorage.getItem('search_product_id'));
            }
            else if (sessionStorage.getItem('search_service_id') != null) {
                // Request service stocks content 
                await requestStocksContent(event, 'service');
            }
            
        });

    }
    else if (document.title == 'Expenses') {
        // Submit expense button
        const submit_expense_button = document.getElementById('submit_expense');
        
        // Check expense button
        const check_expense_button = document.getElementById('check_expense');

        // Add event listener to submit expense button
        submit_expense_button.addEventListener('click', sendExpenseToInsert);

        // Add event listener to check expense button
        check_expense_button.addEventListener('click', requestCheckExpenseResults);

    }
    else if (document.title == 'Human resources') {

        // Select action element
        const select_action_element = document.getElementById('hr_actions');

        // Add event listener to show workers table button
        document.getElementById('workers_table').addEventListener('click', requestWorkersTables);

        // Select worker div element
        const select_worker_div = document.getElementById('select_worker');

        select_action_element.addEventListener('input', function () {
            console.log(select_action_element.value);
            if (select_action_element.value == 'show_absence_form' || select_action_element.value == 'show_benefits_form') {
                // Remove class 'display-none' from select worker div element
                select_worker_div.classList.remove('display-none');
            }
            else {
                // Add class 'display-none' from select worker div element
                select_worker_div.classList.add('display-none');
            }
        })

        // Select action button
        const select_action_button = document.getElementById('human_resources_actions');

        // Add event listener to select action button
        select_action_button.addEventListener('click', async function (event) {
            // Prevent window reload
            event.preventDefault();

            // Select action element value
            const actions = document.getElementsByName('hr_actions_options');

            let action;

            actions.forEach(option => {
                if (option.selected) {
                    action = option.value;
                }
            })

            if (action == 'register_worker_form') {
                // Request register worker form
                await requestRegisterWorkerForm(event);
            }

            else if (action == 'show_absence_form') {
                // Request absence form
                await requestAbsenceForm(event);
            }

            else if (action == 'show_benefits_form') {
                // Request benefits form
                await requestBenefitsForm(event);   
            }

            else {
                // Send error message
                sendErrorMessage(event, 'Please complete the fields.');

                // Add class display-none to select worker element
                select_worker_div.classList.add('display-none');
            }       
        });

    }
    else if (document.title == 'Inventories') {

        // Select action button
        const select_action_button = document.getElementById('inventory_actions');

        // Add event listener to select action button
        select_action_button.addEventListener('click', async function (event) {
            // Prevent window reload
            event.preventDefault();

            // Ensure action is valid
            let action;

            // Action options
            const action_options = document.getElementsByName('inventory_options');

            console.log(action_options);

            // Ensure which action was selected
            action_options.forEach(option => {
                if (option.selected) {
                    action = option.value;
                }
            })

            console.log(action);

            // Valid actions
            const actions = ['create_inventory', 'consult_open_inventories', 'consult_closed_inventories'];

            // Ensure user selected a valid action
            if (!actions.includes(action)) {
                sendErrorMessage(event, 'Select a valid option.')
                throw new Error('Select a valid option.', '404');
            }

            if (action == 'create_inventory') {
                // Request create inventory form
                await requestCreateInventoryForm(event);
            }
            else if (action == 'consult_open_inventories') {
                // Request open inventories
                await requestOpenInventories();
            }
            else {
                // Request consult closed inventories form
                await requestClosedInvetoriesForm();
            }
        })

        // Show pop over with form buttons
        const show_pop_over_form_buttons = document.getElementsByName('show_pop_over_form');

        // Add event listener to show pop over form buttons
        show_pop_over_form_buttons.forEach(button => {
            button.addEventListener('click', async function(event) {
                // Ensure which button was clicked
                if (button.id == 'show_create_inventory_form') {
                    // Request create inventory form
                    await requestCreateInventoryForm(event);
                }

                // Add class show-pop-over to personal-pop-over element
                document.querySelector('.personal-pop-over').classList.add('show-pop-over');

            })
        })

    }
    else if (document.title == 'Sales and wastes analysis') {
        // Analyze date options elements
        const analyze_date_option = document.getElementById('analyze_date_options');

        // Clean sessionStorage
        cleanSessionStorage('search_product_id');
        cleanSessionStorage('search_service_id');
       
        // Add input event listener to options
        analyze_date_option.addEventListener('input', function(event) {
            // Analyze date option
            const analyze_date_option_value = event.target.value;

            console.log(analyze_date_option_value == 'year');

            let next_form_element;

            // Hidden forms
            const hidden_analyze_date_forms = document.getElementsByName('analyze_date_form');

            // Add class 'display-none' from all hidden forms
            hidden_analyze_date_forms.forEach(form => {
                form.classList.add('display-none');
            })

            if (event.target.value == 'year') {
                
                next_form_element = document.getElementById('year_analyze');

            }
            if (event.target.value === 'month') {
                
                next_form_element = document.getElementById('month_analyze');

            }
            if (event.target.value === 'date_period') {

                next_form_element = document.getElementById('two_date_periods');
            }

            // Remove class 'display-none' from next form element
            next_form_element.classList.remove('display-none');

            // Content to analyze select element
            const content_analyze = document.getElementById('content_analyze');
            
            // Remove class 'display-none' from choose content to analyze form
            content_analyze.classList.remove('display-none');

            // Add event listener to content_analize_options select element
            const content_analize_options = document.getElementById('content_analyze_options');

            content_analize_options.addEventListener('input', function(event) {
                // Clean sessionStorage
                cleanSessionStorage('search_product_id');
                cleanSessionStorage('search_service_id');

                // Analyze product or service div element
                const analyze_product_or_service_input = document.getElementById('analize_product_service_input');

                if (event.target.value == 'product' || event.target.value == 'service') {
                    // Remove 'display-none' class
                    analyze_product_or_service_input.classList.remove('display-none');

                    // Description or bar code input
                    const description_bar_code_input = document.getElementById('description_bar_code');
                    

                    if (event.target.value == 'product') {
                        // Add event listener to description input
                        description_bar_code_input.addEventListener('input', async function(event) {
                            // Prevent window reload
                            event.preventDefault();

                            // Clean sessionStorage
                            cleanSessionStorage('search_product_id');
                            cleanSessionStorage('search_service_id');

                            // Request products auto complete
                            requestProductOrServiceAutoComplete(event, "product");
                        });
                    }
                    else if (event.target.value == 'service') {
                        // Add event listener to description input
                        description_bar_code_input.addEventListener('input', async function(event) {
                            // Prevent window reload
                            event.preventDefault();

                            // Clean sessionStorage
                            cleanSessionStorage('search_product_id');
                            cleanSessionStorage('search_service_id');

                            // Request products auto complete
                            requestProductOrServiceAutoComplete(event, "service");
                        });
                    }

                    
                }
                else {
                    // Ensure analyze_product_or_service_input has 'display-none' class
                    if (!analyze_product_or_service_input.classList.contains('display-none')) {
                        // Add class 'display-none'
                        analyze_product_or_service_input.classList.add('display-none');
                    }
                }
            })
        })

        // Analyze sales and wastes button
        const analyze_sales_and_wastes_button = document.getElementById('analyze_sales_and_wastes');

        // Add event listener to analyze sales and wastes button
        analyze_sales_and_wastes_button.addEventListener('click', async function (event) {
            // Prevent window reload
            event.preventDefault();

            // Request charts
            await requestCharts(event)
        });
        
    }
    else if (document.title == 'Mensal reports') {
        // Add event listener to consult mensal reports button
        document.getElementById('consult_mensal_reports').addEventListener('click', async function(event) {
            // Prevent window reload
            event.preventDefault();

            // Get date selected
            const date_selected = document.getElementById('select_mensal_report_date').value;

            await requestMensalReport(event, date_selected);
    })
    }
    else if (document.title == 'Index') {
        // change opacity of buttons in menu index 
        const boxCollection = document.getElementsByClassName("box");
        // Event listener for mouse 
        for (let i = 0; i < boxCollection.length; i++)
        {
            boxCollection[i].addEventListener("mouseover", function() {
                boxCollection[i].style.opacity = 0.5;
            
            });
            boxCollection[i].addEventListener("mouseout", function() {
                boxCollection[i].style.opacity = 1;
            });

        }
        // Event listener for touch
        for (let i = 0; i < boxCollection.length; i++)
        {
            boxCollection[i].addEventListener("touchstart", function() {
                boxCollection[i].style.opacity = 0.5;
            
            });
            boxCollection[i].addEventListener("touchend", function() {
                boxCollection[i].style.opacity = 1;
            });

        }
        
    }
});

// ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------\\ 

// Request analyze sales and wastes charts
async function requestCharts(event) {
    // Prevent window reload
    event.preventDefault();

    // Date option to search
    let date_option_to_search = document.getElementById('analyze_date_options').value;

    let data = [];
    let date;

    // Ensure which date option user selected
    if (date_option_to_search == 'Select analyze date type:') {
        // Send error message and throw error
        sendErrorMessage(event, 'Please select date option to search!');
        throw new Error(`Error: 500, ${'Please select date option to search!'}`)
    }
    else if (date_option_to_search == 'year') {
        // Year analyze options select element
        const year_analyze_option = document.getElementById('year_analyze_options').value;

        // Ensure which year option user selected
        if (year_analyze_option == 'Select year:') {
            // Send error message and throw error
            sendErrorMessage(event, 'Please select year!');
            throw new Error(`Error: 500, ${'Please select year!'}`)
        }
        else {
            date = year_analyze_option;
        }
    }
    else if (date_option_to_search == 'month') {
        // Month analyze options select element
        let month_analyze_option = document.getElementById('month_analyze_options').value;

        // Sanitize month analyze option value
        month_analyze_option = sanitizeInput(month_analyze_option);

        // Ensure which year option user selected
        if (month_analyze_option == 'Select month:') {
            // Send error message and throw error
            sendErrorMessage(event, 'Please select month!');
            throw new Error(`Error: 500, Please select month!`)
        }
        else {
            date = month_analyze_option;
        }
    }
    else if (date_option_to_search == 'date_period') {
        // Start date to analyze
        const start_date = document.getElementById('analyze_start_date').value;

        // End date to analyze
        const end_date = document.getElementById('analyze_end_date').value;
        
        // Ensure start date and end date is not empty
        if (start_date == '' || end_date == '') {
            sendErrorMessage(event, 'Please select dates!');
            throw new Error(`Error: 500, Please select dates!`)
        }
        else {
            date = {start_date: start_date, end_date: end_date};

        }
    }
    else {
        sendErrorMessage(event, 'Please select an option!');
        throw new Error(`Error: 500, Please select an option!`);
    }   

    // Content to analyze select element
    const content_analyze_option = document.getElementById('content_analyze_options').value;

    let request_route;

    // Ensure which year option user selected
    if (content_analyze_option == 'Choose content type:') {
        // Send error message and throw error
        sendErrorMessage(event, 'Please select content type!');
        throw new Error(`Error: 500, 'Please select content type!'`)
    }
    else if (content_analyze_option == 'company') {
        request_route = '/send_company_sales_and_wastes_analysis';

        data = {date_option_to_search: date_option_to_search, date: date};

    }
    else if (content_analyze_option == 'product') {
        request_route = '/send_product_sales_and_wastes_analysis';

        // Product id saved in sessionStorage
        const product_id = sessionStorage.getItem('search_product_id');

        if (product_id == null) {
             // Send error message and throw error
            sendErrorMessage(event, 'Please select product!');
            throw new Error(`Error: 500, 'Please select product!'`)
        }

        data = {date_option_to_search: date_option_to_search, date: date, product_id: product_id};
    }
    else if (content_analyze_option == 'service') {
        request_route = '/send_service_sales_and_wastes_analysis';

        const service_id = sessionStorage.getItem('search_service_id');

        if (service_id == null) {
            // Send error message and throw error
            sendErrorMessage(event, 'Please select service!');
            throw new Error(`Error: 500, 'Please select service!'`)
       }

       data = {date_option_to_search: date_option_to_search, date: date, service_id: service_id};
    }
    else {
        // Send error message and throw error
        sendErrorMessage(event, 'Please select content type!');
        throw new Error(`Error: 500, 'Please select content type!'`)
    }

    // Request charts info
    const chartInfo = await requestChartsInfo(request_route, data);

    if (chartInfo.errorData) {

        sendErrorMessage(event, chartInfo.errorData.error);
        throw new Error(`Error ${chartInfo.status}: ${chartInfo.errorData.error}`);
    }

    // searched_sales_and_wastes.html rendered 
    const sales_and_wastes_analyze_rendered = chartInfo.search_sales_and_wastes_rendered;

    // Insert search_sales_and_wastes_rendered in analysis_content div element
    const analysis_content_element = document.getElementById('analysis_content');
    analysis_content_element.innerHTML = sales_and_wastes_analyze_rendered;

    // Waste motives chart element
    const waste_motives = document.getElementById('topWasteMotives').getContext('2d');

    // Sales and wastes chart info
    const sales_and_wastes_labels = chartInfo.sales_and_wastes_data.labels;
    const wastes = chartInfo.sales_and_wastes_data.wastes;
    const sales = chartInfo.sales_and_wastes_data.sales;
    const chart_title = chartInfo.sales_and_wastes_data.chart_title;

    // Ensure amount of days user want to search and set chart type
    let sales_and_wastes_chart_type;


    // If labels less or equal to five create a chart of bar type, else line
    if (sales_and_wastes_labels.length <= 5) {
        sales_and_wastes_chart_type = 'bar';
    }
    else {
        sales_and_wastes_chart_type = 'line';
    }

    // Elements to insert sales and wastes chart
    const sales_and_wastes_chart = document.getElementById('salesWastesChart').getContext('2d');

    // Create waste and sales chart
    new Chart(sales_and_wastes_chart, {
        type: sales_and_wastes_chart_type,  // Specify the chart type
        data: {
            labels: sales_and_wastes_labels,  // X-axis labels
            datasets: [{
                label: 'Sales',
                data: sales,   // Data points for Dataset 1
                backgroundColor: 'rgb(25, 135, 84, 0.5)',
                borderColor: 'rgba(25, 135, 84, 0.5)',
                borderWidth: 1,
            }, {
                label: 'Wastes',
                data: wastes,   // Data points for Dataset 2
                backgroundColor: 'rgb(255, 0, 0, 0.5)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: chart_title
                },
                legend: {
                    position: 'bottom',
                    align: 'start'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
    
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'EUR' }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });

    // Sales inteverval time
    const interval_time_sales_data = chartInfo.interval_time_sales_data;

    new Chart('salesByHoursInterval', {
        type: "bar",
        data: {
            labels: interval_time_sales_data.interval_time_sales_labels,  
            datasets: [{
                label: 'Sales',
                data: interval_time_sales_data.interval_time_sales,
                backgroundColor: 'rgb(25, 135, 84, 0.5)',
                borderWidth: 1,
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: interval_time_sales_data.chart_title
                },
                legend: {
                    position: 'bottom',
                    align: 'start'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';

                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'EUR' }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            }
        }
      });

    // Wastes and motives data
    const wastes_motives_data = chartInfo.wastes_motives_data;

    new Chart(waste_motives, {
        type: "pie",
        data: {
          labels: wastes_motives_data.motives,
          datasets: [{
            backgroundColor: wastes_motives_data.bar_colors,
            data: wastes_motives_data.wastes_values
          }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    align: 'start'
                },
                title: {
                    display: true,
                    text: "Wastes type values(€)"
                },
                tooltip: {
                    callbacks: {
                        label: function(tooltipItem) {
                            let value = tooltipItem.raw;
                            return '€ ' + new Intl.NumberFormat('de-DE', {
                                style: 'currency',
                                currency: 'EUR',
                            }).format(value);
                        }
                    }
                },
                datalabels: {
                    formatter: function(value, context) {
                        return '€ ' + new Intl.NumberFormat('de-DE', {
                            style: 'currency',
                            currency: 'EUR',
                        }).format(value);
                    }
                }
            },
            legend: {display: true}
        }
    });

    if (content_analyze_option == 'company') {
        // Element to top products units sell create chart
        const top_units_sell_chart = document.getElementById('topUnitsSellProducts').getContext('2d');

        // Unit sells data
        const unit_sells_data = chartInfo.products_units_sell_data;

        // Create top units sell chart
        new Chart(top_units_sell_chart, {
            type: "bar",
            data: {
            labels: unit_sells_data.products_description,
            datasets: [{
                label: "Units sell",
                backgroundColor: unit_sells_data.bar_color,
                data: unit_sells_data.products_units_sell
            }]
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        position: 'bottom',
                        align: 'start'
                    },
                    title: {
                        display: true,
                        text: "Top products units sell"
                    }
                },
                legend: {display: true}
            }
        });

         // Unit sells data
        const services_units_sell_data = chartInfo.services_units_sell_data;

        // Create top units sell chart
        new Chart('topUnitsSellServices', {
                type: "bar",
                data: {
                labels: services_units_sell_data.services_description,
                datasets: [{
                    label: "Units sell",
                    backgroundColor: services_units_sell_data.bar_color,
                    data: services_units_sell_data.services_units_sell
                }]
                },
                options: {
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    },
                    plugins: {
                        legend: {
                            position: 'bottom',
                            align: 'start'
                        },
                        title: {
                            display: true,
                            text: "Top services units sell"
                        }
                    },
                    legend: {display: true}
            }
        });
    }

    
}

// Request Charts info to create charts and return
async function requestChartsInfo(request_route, data) {

    // Request charts info      
    const result = requestServerAndReturnResponse(request_route, data, json=true);

    // Return charts info
    return result;
}

// Remove all products from register list
async function removeAllProductsFromRegisterList(event) {
    // Prevent window from reload
    event.preventDefault();

    // Send request to server
    try {
        // Send request
        const response = await fetch('/remove_all_products_from_register_list', {method: "POST"});

        // Get response
        const result = await response.json();

        // Insert response html in register_list content
        document.getElementById('register_list').innerHTML = result.delete_register_list_sucess_html;

        // Remove show-pop-over class from pop-over element
        document.querySelector('.confirm-pop-over').classList.remove('show-pop-over');
        
    }
    catch (error) {
        console.log(error);
    }
}

// Remove all products from order list
async function removeAllProductsFromOrderList(event) {
    // Prevent window from reload
    event.preventDefault();

    try {
        // Send request to delete all products from order list
        const response = await fetch('/delete_all_products_from_order_list', {method: "POST"});

        // Response result
        const result = await response.json();

        // Send message from response result
        showPopOver(result.sucess_message, "Order deleted with success!");

        await requestOrderTableAndUpdate(0);

    }
    catch (error) {
        console.log(error);
    }
}

// Register products in system
async function registerProducts(event=null, from_order=false) {
    if (event != null) {
        // Prevent window reload
        event.preventDefault();
    }
    try {
        // Send request
        const response = await fetch('/register_products', {method: "POST"});

        // Get response
        const result = await response.json();

        if (!from_order) {
            // Insert response html in register_list content
            document.getElementById('products_and_services_content').innerHTML = result.register_list_sucess_html;

        }        
    }
    catch (error) {
        console.log(error);
    }
}

async function registerOrder(event) {
    if (event) {
        event.preventDefault();
    }
    
    // Get order total
    const order_total = document.getElementById('order_total').getAttribute('value');

    // Get other encharges
    let other_encharges = document.getElementById('other_encharges').value;

    if (other_encharges == '') {
        other_encharges = 0;
    }

    // Order total value
    const order_value = [order_total, other_encharges];
    
    // Request server and get response
    const result = await requestServerAndReturnResponse('/register_order', order_value, json=true);

    // Order content to insert html response
    const order_content_element = document.getElementById('order_content');
         
    order_content_element.innerHTML = result.sucess_order_register_html;

}

async function registerWorker(event, worker_data) {
    
    // Prevent window from reload
    event.preventDefault();

    const result = await requestServerAndReturnResponse('/register_worker', worker_data, json=true)

    // Reset form
    const form = document.querySelector('form');
    form.reset();

    // Send sucess message
    showPopOver(result.success_message, "Register worker");
    
}

// Request register products form and insert in products_and_services_content 
async function requestRegisterProductsForm(event) {
    // Prevent window reload
    event.preventDefault();

    // Request server and get html result response
    const response = await fetch('/send_register_products_form');

    // Response result
    const result = await response.json()

    // Insert result in products_and_services_content
    document.getElementById('products_and_services_content').innerHTML = result.register_products_html;

    // Select element
    const select_category_element = document.getElementById('categories');

    // Add event listener to select category element
    select_category_element.addEventListener('input', async function(event) {

        const data_to_send = {category_id: event.target.value,
                              action: 'product_input' 
        }

        console.log(data_to_send);

        // Request CATEGORY sub categories
        const result = await requestServerAndReturnResponse('/send_sub_categories', data_to_send, json=true);

        // Sub category div element
        const sub_category_select = document.getElementById('sub_categories_content');

        // Remove display-none class from select sub category element
        sub_category_select.classList.remove('display-none');

        // Insert html options with sub categories in select
        sub_category_select.querySelector('select').innerHTML = result.sub_categories_options; 

    })

    // Get validate product register button element
    const send_product_to_validate_register_button = document.getElementById('submit_product');

    // Add event listender to send_product_to_validate_register_button
    send_product_to_validate_register_button.addEventListener('click', async function (event) {
        await sendProductToValidateRegister(event);
    })

    // Button to confirm register
    const confirm_register_button = document.getElementById('confirm_register');

    // Add event listener to confirm register button
    confirm_register_button.addEventListener('click', requestConfirmRegisterHtml);

}

async function  requestRegisterServicesForm(event) {
    // Prevent window reload
    event.preventDefault();

    // Request server and get html result response
    const response = await fetch('/send_register_service_form', {method: "POST"});
 
    // Response result
    const result = await response.json()
 
    // Insert result in products_and_services_content
    document.getElementById('products_and_services_content').innerHTML = result.register_service_html;

    // Handle add or remove product in register service form
    AddOrRemoveProductFromServiceInputHandler();

    // Add event listener to register service button
    document.getElementById('submit_service').addEventListener('click', sendServiceToValidateRegister);

    console.log(document.querySelectorAll('.stock'));

    // Add event listener to stock inputs to get calculated cost price
    document.querySelectorAll('.stock').forEach(input => {
        input.addEventListener('input', requestServiceCalculatedCostPrice);
    })
  
}

// Request edit product form and insert in pop over
async function requestEditProductForm(event) {
    // Prevent window reload
    event.preventDefault();

    // Product id
    const product_id = event.target.closest('tr').id;

    // Request server
    const result = await requestServerAndReturnResponse('/send_edit_product_form', product_id);

    // Show popover
    showPopOver(result.edit_product_form_html, 'Edit product');

    // Add event listener to save changes
    document.getElementById('save_changes').addEventListener('click', async function (event) {
        await sendProductToEdit(product_id, event);
    });

    // Add event listener to delete product
    document.getElementById('delete_product').addEventListener('click', async function (event) {

        showConfirmPopoverAndPersonalize(event, 'delete_product', product_id);
    });

    // Select element
    const select_category_element = document.getElementById('categories');

    // Add event listener to select category element
    select_category_element.addEventListener('input', async function(event) {

        const data_to_send = {category_id: event.target.value,
                              action: 'product_input' 
        }

        console.log(data_to_send);

        // Request CATEGORY sub categories
        const result = await requestServerAndReturnResponse('/send_sub_categories', data_to_send, json=true);

        // Sub category div element
        const sub_category_select = document.getElementById('sub_categories_content');

        // Remove display-none class from select sub category element
        sub_category_select.classList.remove('display-none');

        // Insert html options with sub categories in select
        sub_category_select.querySelector('select').innerHTML = result.sub_categories_options; 

    })
}

// Request edit product form and insert in pop over
async function requestEditServiceForm(event) {
    // Prevent window reload
    event.preventDefault();

    // Product id
    const service_id = event.target.closest('tr').id;

    // Request server
    const result = await requestServerAndReturnResponse('/send_edit_service_form_rendered', service_id);

    // Show content with edit service form inserted
    showPopOver(result.edit_service_form_html, 'Edit service');

    // Handle select services products form
    AddOrRemoveProductFromServiceInputHandler();

    // Add event listener to stock inputs to get calculated cost price
    document.getElementsByName('service_stock').forEach(input => {
        input.addEventListener('input', requestServiceCalculatedCostPrice);
    })

    // Add event listener to save changes
    document.getElementById('save_changes').addEventListener('click', async function (event) {
        await sendServiceToEdit(service_id, event);
    });

    // Add event listener to delete service
    document.getElementById('delete_service').addEventListener('click', async function (event) {
        await showConfirmPopoverAndPersonalize(event, 'delete_service', service_id);
    });

    // Service products and stocks
    const service_products_and_stocks = result.service_products_and_stocks;

    // Simulate click in add_product_button
    const clickEvent = new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: true
    });

    console.log(service_products_and_stocks);
    
    // Itherate service_products_and_stocks
    for (let i = 0; i < service_products_and_stocks.length; i++) {
        // Active input
        const active_input = document.querySelector('.active_select_input');

        // Active input select product options
        const select_product_options = active_input.querySelector('select').querySelectorAll('option');

        console.log(select_product_options);

        // Set selected attribute to select product option if product is in service_products_and_stocks
        select_product_options.forEach(option => {
            if (Number(option.value) == service_products_and_stocks[i].product_id) {
                option.selected = true;
            }
        })

        // Set service product stock in stock input
        active_input.querySelector('.stock').value = service_products_and_stocks[i].stock;

        // Add product button
        const add_product_button = document.getElementById('add_select_input');

        add_product_button.dispatchEvent(clickEvent);
    }

    document.getElementById('remove_select_input').dispatchEvent(clickEvent);

    // Request service calculated cost price
    requestServiceCalculatedCostPrice();
   
}

async function requestEditWorkerForm (event, worker_id) {
    // Prevent window reload
    event.preventDefault();

    // Request change product form html
    try {
        // Get response
        const result = await requestServerAndReturnResponse('/send_edit_worker_form', worker_id);

        if (result.errorData) {

            sendErrorMessage(event, result.errorData.error);
            throw new Error(`Error ${result.status}: ${result.errorData.error}`);
        }

        showPopOver(result.edit_worker_form, 'Edit worker');

        // Popover button to save changes
        const save_worker_edit_changes = document.getElementById('save_changes_worker');

        // Popover button to delete worker
        const delete_worker_button = document.getElementById('delete_worker');

        // Add event listener to save changes in workers button
        save_worker_edit_changes.addEventListener('click', async function(event) {
            // Prevent window reload
            event.preventDefault();

            // Send Worker to validate
            await sendWorkerToValidate(event, register=false, edit=true);
            
        });

        // Add event listener to delete worker button
        delete_worker_button.addEventListener('click', sendWorkerToDelete);

        // Add event listener to back to workers table
        document.getElementById('back_to_workers_table').addEventListener('click', requestWorkersTables);

    }
    catch (error) {
        console.log(error);
    }
}

// Request benefits form and insert in popover
async function requestBenefitsForm(event) {
    // Prevent window reload
    event.preventDefault();

    // Get all option elements with name 'benefit_assign_worker'
    const benefit_register_worker_options = document.getElementsByName('select_worker');

    let worker_id;

    // Check which options is select and get worker id
    benefit_register_worker_options.forEach(option => {
        if (option.selected) {
            worker_id = option.value;
        }
    })

    // Response result
    const result = await requestServerAndReturnResponse('/send_benefit_form', worker_id);

    // Ensure theres no errros
    if (result.errorData) {

        showPopOver(result.errorData.error, "Error");
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Benefit form
    const benefit_form = result.benefit_form;
    
    // Insert content in popover
    showPopOver(benefit_form, "Benefits");

    // Register absence button
    const assing_benefit_button = document.getElementById('register_benefit');

    // Add event listener to register absence button
    assing_benefit_button.addEventListener('click', async function(event) {
        await sendBenefitToValidateAndRegister(event, worker_id);
    })

    // Consult absences button
    const consult_benefits_button = document.getElementById('consult_benefits');

    // Add event listener to consult absence button
    consult_benefits_button.addEventListener('click', async function(event) {

        await requestBenefitsConsultResultsAndInsert(event, worker_id);
    })
}

// Requesr register worker form
async function requestRegisterWorkerForm(event) {
    // Prevent window reload
    event.preventDefault();

    // Request server
    const response = await fetch('/send_register_worker_form', {method:"POST"});

    // Get result
    const result = await response.json();

    // Insert response result in hr_action_content
    showPopOver(result.register_worker_form, "Register worker");

    // Register worker button
    const register_worker_button = document.getElementById('register_worker');

    // Add event listener to register worker button
    register_worker_button.addEventListener('click', async function(event) {
        // Prevent window from reload
        event.preventDefault();
    
        // Send worker data to validate and register
        await sendWorkerToValidate(event, register=true);
    });
}

async function requestAbsenceForm(event) {
    // Prevent window reload
    event.preventDefault();
   
        // Get all option elements with name 'abstence_register_worker'
        const abstence_register_worker_options = document.getElementsByName('select_worker');

        let worker_id;

        // Check which options is selected and get worker id
        abstence_register_worker_options.forEach(option => {
            if (option.selected) {
                worker_id = option.value;
            }
        })

        // Send request with worker id
        const result = await requestServerAndReturnResponse('/send_absence_form', worker_id)

        if (result.errorData) {

            sendErrorMessage(event, result.errorData.error);
            throw new Error(`Error ${result.status}: ${result.errorData.error}`);
        }

        // Abstence form
        const abstence_form = result.abstence_form;

        // Show popover and insert content
        showPopOver(abstence_form, "Absences");

        // Register absence button
        const register_absence_button = document.getElementById('register_absence');

        // Add event listener to register absence button
        register_absence_button.addEventListener('click', async function(event) {
            await sendAbsenceToValidateAndRegister(event, worker_id);
        })

        // Consult absences button
        const consult_absence_button = document.getElementById('consult_absences');

        // Add event listener to consult absence button
        consult_absence_button.addEventListener('click', async function(event) {

            await requestAbsencesConsultResults(event, worker_id);
        })
}

// Request count_inventory_form_html
async function requestCountInventoryForm(event, inventory_id, pagination_index) {
    // Prevent window reload
    event.preventDefault();

    // Data
    const data = {
        inventory_id: inventory_id,
        pagination_index: pagination_index};

    // Request server and get response
    const result = await requestServerAndReturnResponse('/send_count_inventory_form', data, json=true);

    // Ensure response has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Insert count_inventory_form_html in popover body content
    document.querySelector('.pop-over-content-body').innerHTML = result.count_inventory_form_html;

    // Count inputs
    const count_inputs = document.getElementsByName('count_input');

    // Storaged inventory data
    storaged = JSON.parse(sessionStorage.getItem(inventory_id));
    
    // Ensure sessionStorage has storaged inventory data
    if (storaged != null) {
                
        count_inputs.forEach(input => {
            
            // Assign already saved values in inventory counts input
            for (let i=0; i < storaged.length; i++) {
                if (input.id == storaged[i].product_id) {
                    
                    input.value = storaged[i].stock_value;
                }
            }
        })
    }

    // Storage inventory counts
    storageInventoryCounts(inventory_id);

    // Add show-pop-over class to popover element
    document.querySelector('.personal-pop-over').classList.add('show-pop-over');

    // Change popover title
    document.getElementById('edit_title').innerHTML = 'Count inventory'

    // Submit counts button
    const submit_count_button = document.getElementById('submit_counts');
    
    // Add event listener to submit counts
    submit_count_button.addEventListener('click', async function(event) 
        {
            await sendInventoryCounts(event, inventory_id);
        }
    );

    // Change page buttons from pagination navbar
    const change_page_buttons = document.getElementsByName('change_page');

    // Add event listener to change page buttons
    change_page_buttons.forEach(button => {
        button.addEventListener('click', function (event) {
            handlePaginationButtonsAndUpdateResults(event, "count_inventory", inventory_id);
        })            
    })
}

// Request finish_inventory_form.html and insert in popover
async function requestFinishInventoryForm(event, inventory_id, pagination_index) {
    // Prevent window reload
    event.preventDefault();

    console.log("finish")

    // Data
    const data = {
        inventory_id: inventory_id,
        pagination_index: pagination_index};

    console.log(data);
    
    // Request server and get response
    const result = await requestServerAndReturnResponse('/send_finish_inventory_form', data, json=true);

    // Ensure response has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Insert count_inventory_form_html in popover body content
    document.querySelector('.pop-over-content-body').innerHTML = result.finish_inventory_form_html;

    // Add show-pop-over class to popover element
    document.querySelector('.personal-pop-over').classList.add('show-pop-over');

    // Change popover title
    document.getElementById('edit_title').innerHTML = 'Finish inventory';

    // Products check recount inputs
    const recount_check_inputs = document.getElementsByName('send_to_recount');

    // Finish inventory button
    const finish_inventory_button = document.getElementById('finish_inventory');

    if (!finish_inventory_button.disabled) {
        finish_inventory_button.addEventListener('click', async function(event) {
            await sendInventoryToFinish(event, inventory_id);
        })

    }

    // Send to recount button
    const send_to_recount_button = document.getElementById('send_recount');

    // Use sessionStorage to save products to recount
    storageInventoryProductsToRecount(inventory_id);

    // Storaged data in sessionStorage with products ids already checked
    let storaged_data = JSON.parse(sessionStorage.getItem(inventory_id));

    console.log(storaged_data);

    // Ensure storaged data is not empty
    if (storaged_data != null) {
        if (storaged_data.length != 0) {
            
            // Itherite recount check inputs
            recount_check_inputs.forEach(check => {
                
                // Get product id
                const product_id = check.id;

                console.log(product_id);

                // Ensure product id is in storaged data
                if (storaged_data.includes(product_id)) {
                    // Changed check input to checked
                    check.checked = true;
                }

            })

            // Add event listener to send products to recount button
            send_to_recount_button.addEventListener('click', async function() {
                // Send products to recount 
                await sendProductsToRecountInventory(event, inventory_id)});

            // Remove class 'display-none' from send_to_recount_button
            send_to_recount_button.classList.remove('display-none')

            // Add class 'display-none' to finish inventory button
            finish_inventory_button.classList.add('display-none');
            }
    }

    // Add event listener to chek recount inputs
    recount_check_inputs.forEach(check => {
        check.addEventListener('input', function() {

        // Storaged data in sessionStorage with products ids already checked
        storaged_data = JSON.parse(sessionStorage.getItem(inventory_id));

        if (storaged_data == null || storaged_data.length == 0) {
            // Remove class 'display-none' from fiish inventory button
            finish_inventory_button.classList.remove('display-none')

            // Add class 'display-none' to send_to_recount_button
            send_to_recount_button.classList.add('display-none');

            // Add event listener to finish inventory button
            finish_inventory_button.addEventListener('click', async function (event) {
                // Send inventory to finish
                await sendInventoryToFinish(event, inventory_id);
            });

        }
        else {
            // Remove class 'display-none' from send_to_recount_button
            send_to_recount_button.classList.remove('display-none')

            // Add class 'display-none' to finish inventory button
            finish_inventory_button.classList.add('display-none');

            // Add event listener to send_to_recount_button
            send_to_recount_button.addEventListener('click', async function() {
                // Send products to recount 
                await sendProductsToRecountInventory(event, inventory_id)});

            }
        })
    })

    // Change page buttons from pagination navbar
    const change_page_buttons = document.getElementsByName('change_page');

    // Add event listener to change page buttons
    change_page_buttons.forEach(button => {
        button.addEventListener('click', function (event) {
            handlePaginationButtonsAndUpdateResults(event, "finish_inventory", inventory_id);
        })            
    }) 
}

async function requestRecountInventoryForm(event, inventory_id, pagination_index) {
    // Prevent window reload
    event.preventDefault();

    // Data
    const data = {
        inventory_id: inventory_id,
        pagination_index: pagination_index};

    // Request server and get response
    const result = await requestServerAndReturnResponse('/send_recount_inventory_form', data, json=true);
 
    // Ensure response has no errors
    if (result.errorData) {
 
        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }
 
    // Insert count_inventory_form_html in popover body content
    document.querySelector('.pop-over-content-body').innerHTML = result.recount_inventory_form_html;

    storageInventoryCounts(inventory_id);
 
    // Add show-pop-over class to popover element
    document.querySelector('.personal-pop-over').classList.add('show-pop-over');
 
    // Change popover title
    document.getElementById('edit_title').innerHTML = 'Recount inventory'
 
    // Submit counts button
    const submit_recount_button = document.getElementById('submit_recounts');
     
    // Add event listener to submit counts
    submit_recount_button.addEventListener('click', async function(event) {
            // Send inventory recounts 
            await sendInventoryRecounts(event, inventory_id);
         }
    );

    // Change page buttons from pagination navbar
    const change_page_buttons = document.getElementsByName('change_page');

    // Add event listener to change page buttons
    change_page_buttons.forEach(button => {
        button.addEventListener('click', function (event) {
            handlePaginationButtonsAndUpdateResults(event, "count_inventory", inventory_id);
        })            
    }) 

}

// Request consult closed inventories form
async function requestClosedInvetoriesForm() {
    // Request server
    const response = await fetch('/render_consult_closed_inventories_form', {method: "POST"});

    const result = await response.json();
    
    // Insert result
    document.getElementById('inventories_action_content').innerHTML = result.consult_closed_inventories_form_html;

    // Consult inventories button
    const consult_inventory_dates = document.getElementById('consult_inventory_dates');

    if (consult_inventory_dates) {
        // Add event listener to consult closed inventories button
        consult_inventory_dates.addEventListener('click', requestClosedInventories);
    }
}

async function requestCreateInventoryForm(event) {
    // Prevent window reload
    event.preventDefault();

    // Request server with family and get create inventory form
    const result = await requestServerAndReturnResponse('/send_create_inventory_form');

    // New inventory storage data
    const new_inventory_storaged_data = JSON.parse(sessionStorage.getItem('new_inventory'));

    // Ensure session is not empty
    if (new_inventory_storaged_data != null) {
        // Clean sessionStorage new inventory
        sessionStorage.clear('new_inventory');
    }

    // Ensure result response has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }
    
    // Insert form
    document.getElementById('inventories_action_content').innerHTML = result.create_inventory_form;

    console.log('inventory form inserted');

    // Select element
    const select_category_element = document.getElementById('category');

    console.log(select_category_element);

    // Add event listener to select category element
    select_category_element.addEventListener('input', async function() {

        let category_id;

        // Category options
        const category_options = select_category_element.querySelectorAll('option');

        console.log(category_options);

        // Sub category content div element
        const sub_category_check = document.getElementById('select_sub_categories');

        // Check which category is selected and get category id
        let able_to_send = false;

        category_options.forEach(option => {
            if (option.selected) {
                if (option.value == 'All') {
                    sub_category_check.classList.add('display-none');
                }
                else {
                    // Remove display-none class from select sub category element
                    sub_category_check.classList.remove('display-none');

                    category_id = option.value;

                    able_to_send = true;
                }
            }
        })

        if (able_to_send) {

            const data_to_send = {category_id: category_id, action: 'product_search', csrf_token: document.getElementById('csrf_token').value};

            // Request CATEGORY sub categories
            const result = await requestServerAndReturnResponse('/send_sub_categories', data_to_send, json=true);

            // Insert html options with sub categories in check buttons
            sub_category_check.innerHTML = result.sub_categories_options;
        } 
    })

    // Submit categories selected to get products button
    const select_products_button = document.getElementById('select_products_to_inventory');

    // Add event listener to select_products_button
    select_products_button.addEventListener('click', async function(event) {
        // Prevent window reload
        event.preventDefault();

        // Request categories products to select to create inventory
        await requestSelectProductsToInventoryForm(event, 0);
    });
}

// Request server change company name form
async function requestChangeCompanyNameForm() {
    // Request change company name form
    const result = await requestServerAndReturnResponse('/send_change_company_name_form');
    
    showPopOver(result.change_company_name_form, 'Change company name');

    // Add event listener to confirm change company name
    document.getElementById('confirm_change').addEventListener('click', async function(event) {
        // Prevent window reload
        event.preventDefault();

        // Get form element
        const change_company_name_form_element = document.getElementById('change_company_name_form');

        // Request server to validate Form
        await validateForm(event, change_company_name_form_element, '/validate_change_company_name');

    })
}

async function requestChangeEmailForm() {
    // Request change company name form
    const result = await requestServerAndReturnResponse('/send_change_email_form');
    
    showPopOver(result.change_email_form, '<span style="color:green;">Authenticated with success!</span>');

    // Add event listener to confirm change company name
    document.getElementById('confirm_change').addEventListener('click', async function(event) {
        // Prevent window reload
        event.preventDefault();

        // Get form element
        const change_email_form_element = document.getElementById('change_email_form');

        // Request server to validate Form
        await validateForm(event, change_email_form_element, '/validate_change_email');

        // Logout and redirect to login route in 3 seconds
        logoutUserAndRedirectToLogin();
    })

}

async function requestChangePasswordForm() {
    // Request change company name form
    const result = await requestServerAndReturnResponse('/send_change_password_form');
    
    showPopOver(result.change_password_form, '<span style="color:green;">Authenticated with success!</span>');

    // Add event listener to confirm change company name
    document.getElementById('confirm_change').addEventListener('click', async function(event) {
        // Prevent window reload
        event.preventDefault();

        // Get form element
        const change_password_form_element = document.getElementById('change_password_form');

        // Request server to validate Form
        await validateForm(event, change_password_form_element, '/validate_change_password');

        // Logout and redirect to login route in 3 seconds
        logoutUserAndRedirectToLogin();

    })
}

async function requestChangePersonalCodeForm() {
     // Request change company name form
     const result = await requestServerAndReturnResponse('/send_change_personal_code_form');
    
     showPopOver(result.change_personal_code_form, '<span style="color:green;">Authenticated with success!</span>');
 
     // Add event listener to confirm change company name
     document.getElementById('confirm_change').addEventListener('click', async function(event) {
         // Prevent window reload
         event.preventDefault();
 
        // Get form element
        const change_password_form_element = document.getElementById('change_personal_code_form');
 
        // Request server to validate Form
        await validateForm(event, change_password_form_element, '/validate_change_personal_code');

        // Logout and redirect to login route in 3 seconds
        logoutUserAndRedirectToLogin();
     })
}

// Request server change company name form
async function requestChangeCurrencyForm() {
    // Request change company name form
    const result = await requestServerAndReturnResponse('/send_change_currency_form');
    
    showPopOver(result.change_currency_form, 'Change currency');

    // Add event listener to confirm change company name
    document.getElementById('confirm_change').addEventListener('click', async function(event) {
        // Prevent window reload
        event.preventDefault();

        // Get form element
        const change_currency_form_element = document.getElementById('change_currency_form');

        // Request server to validate form
        await validateForm(event, change_currency_form_element, '/validate_change_currency');
    })
}

async function requestConfirmRegisterHtml(event) {
    // Prevent window reload
    event.preventDefault();

    // Request server and get html result response
    const response = await fetch('/send_confirm_register_html', {method: "POST"});

    // Response result
    const result = await response.json()

    // Insert result in products_and_services_content
    document.getElementById('products_and_services_content').innerHTML = result.confirm_register_html;

    // Get remove product from list buttons
    const remove_product_buttons = document.querySelectorAll('.remove_product_from_register_list');

    // Get confirm_remove_all_products_from_register_list button
    const confirm_remove_all_products_from_register_list_button = document.getElementById('confirm_remove_all_products_from_register_list');

    // Get confirm_register_products button
    const confirm_register_button = document.getElementById('confirm_register_products');

    // Add event listeners to remove product from list, remove all products from list and confirm register products buttons
    remove_product_buttons.forEach(button => {
        button.addEventListener('click', async function(event) {
            await sendProductToRemoveFromRegisterList(event)
        });
   })
    
    confirm_remove_all_products_from_register_list_button.addEventListener('click', function(event) {
        showConfirmPopoverAndPersonalize(event, confirm_remove_all_products_from_register_list_button.value);
    }) 

    confirm_register_button.addEventListener('click', function(event) {
        showConfirmPopoverAndPersonalize(event, confirm_register_button.value);  
    })

}

async function requestMyProductsAndServicesHtml(event) {
    // Prevent window reload
    event.preventDefault();

    // Request server and get html result response
    const response = await fetch('/send_my_products_and_services_rendered');

    // Response result
    const result = await response.json()

    // Insert result in products_and_services_content
    document.getElementById('products_and_services_content').innerHTML = result.my_products_and_services_html;

    // Type filter select element
    const type_filter_select = document.getElementById('type_filter');

    // Select category div element
    const select_category = document.getElementById('select_category');

    // Select sub category div element
    const select_sub_category = document.getElementById('select_sub_categories');

    // Add event listener to type_filter_select
    type_filter_select.addEventListener('input', function () {
        if (type_filter_select.value == 'product') {
            // Remove 'display-none' class
            select_category.classList.remove('display-none');
        }
        else {
            select_category.classList.add('display-none');
            select_sub_category.classList.add('display-none');
        }
    })

    // Get search button
    const search_button = document.getElementById('submit_search_all');

    // Select element
    const select_category_element = document.getElementById('category_filter');

    // Add event listener to select category element
    select_category_element.addEventListener('input', async function() {

        let category_id;

        // Category options
        const category_options = select_category_element.querySelectorAll('option');

        // Sub category div element
        const sub_category_check = document.getElementById('select_sub_categories');

        // Get form csrf token element
        const csrf_token = document.getElementById('csrf_token');

        // Check which category is selected and get category id
        let able_to_send = false;

        category_options.forEach(option => {
            if (option.selected) {
                if (option.value == 'All') {
                    sub_category_check.classList.add('display-none');
                }
                else {
                    // Remove display-none class from select sub category element
                    sub_category_check.classList.remove('display-none');

                    category_id = option.value;

                    able_to_send = true;
                }
            }
        })

        if (able_to_send) {
            const data_to_send = {category_id: category_id,
                action: 'product_search',
                csrf_token: csrf_token.value};

            // Request CATEGORY sub categories
            const result = await requestServerAndReturnResponse('/send_sub_categories', data_to_send, json=true);

            // Insert html options with sub categories in select
            sub_category_check.innerHTML = result.sub_categories_options;
        } 
    })

    // Add event listener to search button
    search_button.addEventListener('click', async function (event) {
        requestMyProductsAndServiceSearchFilters(event, 0);
    });

}

async function requestEditProductsAndServicesHtml(event) {
    // Prevent window reload
    event.preventDefault();

    // Request server and get html result response
    const response = await fetch('/send_edit_products_and_services_rendered', {method: "POST"});
 
    // Response result
    const result = await response.json()
 
    // Insert result in products_and_services_content
    document.getElementById('products_and_services_content').innerHTML = result.edit_products_and_services_html;

    // Search button
    const search_product_and_service_button = document.getElementById('submit_search_and_edit');

    // Add event listener to search button
    search_product_and_service_button.addEventListener('click', async function(event) {
        await requestProductOrServiceSearchToEdit(event);
    });

}

// Request calculated service cost price
async function requestServiceCalculatedCostPrice() {

    // Convert data from form to formData object
    const form_data = new FormData(document.getElementById('service_form'));
    
    // Convert form_data to a JSON object
    const form_object = Object.fromEntries(form_data.entries());

    const result = await requestServerAndReturnResponse('/send_calculated_service_cost_price', form_object, json=true);

    document.getElementById('service_calculated_cost_price').innerHTML = result.cost_price_message;
}

async function requestProductOrServiceSearchToEdit(event) {
    // Prevent window reload
    event.preventDefault();

    // Convert data from form to formData object
    const form_data = new FormData(document.getElementById('search_and_edit_form'));
    
    // Convert form_data to a JSON object
    const form_object = Object.fromEntries(form_data.entries());

    for (let i=0; i < form_object.length; i++) {
        form_object[i] = sanitizeInput(form_object[i]);
    }

    // Request server with value to search and get response
    const result = await requestServerAndReturnResponse('/send_products_or_services_edit_search_results', form_object, json=true);

    
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Insert result
    document.getElementById('search_results').innerHTML = result.edit_search_results_html;

    // Edit product rows
    const edit_product_rows = document.querySelectorAll('.edit_product');

    // Itherate edit_product_rows
    edit_product_rows.forEach(row => {
        // Add event listener
        row.addEventListener('click', async function(event) {
            // Add 'show-pop-over' class to personal-pop-over element
            document.querySelector('.personal-pop-over').classList.add('show-pop-over');

            // Request edit product form and insert
            await requestEditProductForm(event);
        })

    })

    // Edit service rows
    const edit_service_rows = document.querySelectorAll('.edit_service');

    // Itherate edit_product_rows
    edit_service_rows.forEach(row => {
        // Add event listener
        row.addEventListener('click', async function(event) {
            // Add 'show-pop-over' class to personal-pop-over element
            document.querySelector('.personal-pop-over').classList.add('show-pop-over');
            // Request edit product form and insert
            await requestEditServiceForm(event);
        })
    })
}

// Request product stock information
async function requestProductStockInfo(event, type)  {
    // Prevent window from reload
    event.preventDefault();

    const options_name = type + '_products';

    // Get select element product options
    const select_product_options = document.getElementsByName(options_name); 
    
    let product_description;
    
    // Get selected item
    select_product_options.forEach(option => {
        if (option.selected) {
            product_description = option.value;
        }
    })

    // Request server and return response
    const result = await requestServerAndReturnResponse('/send_product_stock_info', product_description);

    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Return product stock information
    return result.product_stock_info;
}

// Request updated order table
async function requestOrderTableAndUpdate(pagination_index) {
    
    try {
        // Response result
        const result = await requestServerAndReturnResponse('/send_rendered_order_table', pagination_index) 

        // Insert rendered table
        document.getElementById('order_table').innerHTML = result.order_table_html;

        // Add event listener to delete product from order list button
        document.getElementsByName('delete_product_from_order_list').forEach(button => {
            button.addEventListener('click', sendProductAndDeleteFromOrderList);
        });

        // Order table rows
        const order_rows = document.querySelectorAll('.order_row');

        // Register order button
        const register_order_button = document.getElementById('register_order');
        
        // Delete all products from order button
        const delete_all_products_from_order = document.getElementById('delete_products_from_order');

         // Ensure order is empty or not
        if (order_rows.length == 0) {
            register_order_button.disabled = true;
            delete_all_products_from_order.disabled = true;
        }
        else {
            register_order_button.disabled = false;
            delete_all_products_from_order.disabled = false;
        }

        // Change page buttons from pagination navbar
        const change_page_buttons = document.getElementsByName('change_page');

        // Add event listener to change page buttons
        change_page_buttons.forEach(button => {
            button.addEventListener('click', function (event) {
                handlePaginationButtonsAndUpdateResults(event, "order_table");
            })     
        })

    }
    catch(error) {
        console.log(error);
    }
}

async function requestProductOrServiceAutoComplete(event, search_for) {
    // Event target value
    const input_value = event.target.value;

    console.log(input_value);

    // Autocomplete ul element
    const autocomplete_ul_element = document.getElementById('description_auto_complete');

    if (input_value == '') {
        autocomplete_ul_element.innerHTML = '';
    }

    // Request server 
    const response = await fetch('/search_autocomplete?q=' + input_value + '?' + search_for);

    // Response products
    let search_results = await response.json();

    search_results = search_results.search_results;
    console.log(search_results);
    
    if (search_results) {

        list_html = ''

        let results_index = 0

        for (let i = 0; i < search_results.length; i++) {
            list_html += `<button type='button' name='autocomplete_product' id='${results_index}' class='list-group-item list-group-item-action p-1' aria-current='true'>${search_results[i]['description']} - ${search_results[i]['bar_code']} - ${search_results[i]['unity_m']}</button>`;
            results_index += 1

        }
        
        // Insert response in closest ul element
        autocomplete_ul_element.innerHTML = list_html;

        // Add event listener to autocomplete product buttons
        document.getElementsByName('autocomplete_product').forEach(button => {
            button.addEventListener('click', function(event) {
                // Button index
                const button_index = event.target.id;

                // Product information
                const description = search_results[button_index].description;
                const bar_code = search_results[button_index].bar_code;
                const cost_price = search_results[button_index].cost_price;
                const sell_price = search_results[button_index].sell_price;
                const unity_m = search_results[button_index].unity_m;
                const type = search_results[button_index].type;

                // Insert product or service info in inputs
                const description_input = document.getElementById('description');
                const bar_code_input = document.getElementById('bar_code');
                const cost_price_input = document.getElementById('cost_price');
                const sell_price_input = document.getElementById('sell_price');
                const description_bar_code_input = document.getElementById('description_bar_code');
                const service_description_input = document.getElementById('service_description_bar_code');
                const pos_registry_description_input = document.getElementById('insert_product_or_service');

                // Ensure input exists and set value
                if (description_input) {
                    description_input.value = description;
                }
            
                if (bar_code_input) {
                    bar_code_input.value = bar_code;
                }

                if (cost_price_input) {
                    cost_price_input.value = cost_price;
                }

                if (sell_price_input) {
                    sell_price_input.value = sell_price;
                }

                if (description_bar_code_input) {
                    description_bar_code_input.value = description;
                }

                if (search_for === 'product') {

                    sessionStorage.setItem('search_product_id', search_results[button_index].id);
                   
                }
                else if (search_for === 'service') {

                    if (service_description_input) {
                        service_description_input.value = description;
                    }

                    sessionStorage.setItem('search_service_id', search_results[button_index].id);
                    
                }
                else if (search_for === 'order_product') {

                    sessionStorage.setItem('order_product', search_results[button_index].id);
                }
                else if (search_for === 'pos_registry_product_or_service') {

                    pos_registry_description_input.value = `${description} / ${bar_code} / ${unity_m}`;

                    localStorage.setItem('pos_registry', JSON.stringify([{id: search_results[button_index].id, sell_price: sell_price, unity_m: unity_m, type: type}]));

                    document.getElementById('bar_code').innerHTML = bar_code;

                    console.log(JSON.parse(localStorage.getItem('pos_registry')));
                }

                autocomplete_ul_element.innerHTML = '';


            })
        })

    }
}

async function requestStocksContent(event, request_for) {
    // Prevent window reload
    event.preventDefault();

    // Product id
    const request_for_id = sessionStorage.getItem(`search_${request_for}_id`);

    console.log(`search_${request_for}_id`);

    // Action
    let action = document.getElementById('stock_actions').value;

    // Data to send
    data = {product_or_service_id: request_for_id,
        action: action,
        request_for: request_for};

    console.log(data);

    // Request server and get response
    const result = await requestServerAndReturnResponse(`/send_product_or_service_stocks_content`, data, json=true);

    // Ensure theres no errors in response result
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    console.log(request_for);

    if (result.rendered_register_waste_html) {

        showPopOver(result.rendered_register_waste_html, 'Register waste');

    
        // Add event listener to save regularization button 
        document.getElementById('submit_waste').addEventListener('click', async function(event) {
            // Prevent window reload
            event.preventDefault();
            
            // Send product to regularize with product description and stock to change
            await sendProductOrServiceToWasteOrRegularize(event, request_for_id, "waste", request_for);

        })

    }
    else if (result.rendered_register_regularization_html) {
        showPopOver(result.rendered_register_regularization_html, 'Register regularizaarion');

        // Add event listener to save regularization button 
        document.getElementById('submit_regularization').addEventListener('click', async function(event) {
            event.preventDefault();
   
            // Send product to regularize with id and stock to change
            await sendProductOrServiceToWasteOrRegularize(event, request_for_id, "regularize", request_for);
        })
    }
    else {
        showPopOver(result.rendered_consult_movements_form_html, 'Consult movements');
        
        // Add event listener to consult movements button
        document.getElementById('consult_movements').addEventListener('click', async function(event) {
            // Prevent window reload
            event.preventDefault();
            
            // Request Product Movements
            await requestProductOrServiceMovements(event, request_for_id, 0, request_for);
    
        });
    }
}

async function requestProductOrServiceMovements(event, product_or_service_id, pagination_index, request_for) {
    // Prevent window reload
    event.preventDefault();

    // Start date
    const start_date = document.getElementById('start_date').value;

    // End date
    const end_date = document.getElementById('end_date').value;

    const data = {start_date: start_date, end_date: end_date, product_or_service_id: product_or_service_id, pagination_index: pagination_index};

    // Request movements with product_id and dates
    const result = await requestServerAndReturnResponse(`/send_${request_for}_movements`, data, json=true);

    // Ensure theres no errors in response result
    if (result.errorData) {

        sendErrorMessage(event, '');

        // Movements message element
        const movements_message_element = document.querySelector('.consult_movements_message');

        // Insert error message
        movements_message_element.innerHTML = result.errorData.error;

        setTimeout(function () {
            movements_message_element.innerHTML = '';
        }, 6000)

        throw new Error(`Error ${result.status}: ${result.errorData.error}`);

    }

    showPopOver(result.rendered_movements_html, 'Movements');

    // Change page buttons from pagination navbar
    const change_page_buttons = document.getElementsByName('change_page');

    // Add event listener to change page buttons
    change_page_buttons.forEach(button => {
        button.addEventListener('click', function (event) {
            handlePaginationButtonsAndUpdateResults(event, "movements_table", product_or_service_id, request_for);
        })
            
    })
}

async function requestCheckExpenseResults(event) {
    // Prevent window reload
    event.preventDefault();

    // Validate request expenses form
    await validateForm(event, document.getElementById('check_expense_form'), '/send_check_expenses_result');

    /*
    // Expense check month
    const check_month = document.getElementById('search_expense_month').value;

    // Expense check year
    const check_year = document.getElementById('search_expense_year').value;

    // Insert dates
    const insert_dates = document.getElementsByName('insert_date_option');

    const dates = [];

    insert_dates.forEach(option => {
        dates.push(option.value);
    })

    const expense_data_to_check = {check_month: check_month,
                                   check_year: check_year,
                                   dates: dates};

    // Request server with expense data to check and return response
    const result = await requestServerAndReturnResponse('/send_rendered_check_expenses_result', expense_data_to_check, json=true);

    // Add 'show-pop-over' class to personal-pop-over
    document.querySelector('.personal-pop-over').classList.add('show-pop-over');

    // Change title
    document.getElementById('edit_title').innerHTML = 'Expenses';
    
    // Insert into pop-over-content-body result
    document.querySelector('.pop-over-content-body').innerHTML = result.check_expenses_result;

    */
    
    // Delete expense buttons
    const delete_expense_buttons = document.getElementsByName('delete_expense');

    if (delete_expense_buttons) {
        delete_expense_buttons.forEach(button => {
            button.addEventListener('click', sendExpenseToDelete);
        })
    }
}


// Request workers table html
async function requestWorkersTables(event) {
    // Prevent window reload
    event.preventDefault();

    try {
        // Send request
        const response = await fetch('/send_rendered_workers_tables', {method: "POST"})

        // Response result
        const result = await response.json();
        
        showPopOver(result.rendered_workers_tables, 'Workers');

        // Workers data rows
        const data_rows = document.getElementsByName('worker_data_row');

        // Add event listener to all workers rows to show worker pop over when clicked
        if (data_rows) {
            data_rows.forEach(row => {
                row.addEventListener('click', async function(event) {
                    // Worker id
                    const worker_id = event.target.closest('tr').id;

                    // Request edit worker form
                    await requestEditWorkerForm(event, worker_id);
                    
                })
            })
        }
    }
    catch (error) {

        console.log(error);
    }
}

async function requestWorkerDataAndInsertInEditForm(event) {
    // Worker id
    const worker_id = event.target.closest('tr').id;

    // Send request with worker number
    const result = await requestServerAndReturnResponse('/send_worker_data', worker_id)

    // Ensure theres no errors in response result
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    const worker_data = result.worker_data;

    // Edit input forms
    const worker_id_input = document.getElementById('worker_id');
    const fullname_input = document.getElementById('edit_worker_fullname');
    const adress_input = document.getElementById('edit_worker_adress');
    const born_date_input = document.getElementById('edit_worker_born_date');
    const contact_input = document.getElementById('edit_worker_contact');
    const section_input = document.getElementById('edit_worker_section');
    const role_input = document.getElementById('edit_worker_role');
    const workload_day_input = document.getElementById('edit_worker_workload_day');
    const workload_week_input = document.getElementById('edit_worker_workload_week');
    const base_salary_input = document.getElementById('edit_worker_base_salary');

    // Insert worker info in respective edit inputs
    worker_id_input.innerHTML = worker_id;

    fullname_input.value = worker_data.fullname;
    fullname_input.name = worker_data.fullname;

    adress_input.value = worker_data.adress;
    adress_input.name = worker_data.adress;

    born_date_input.value = worker_data.born_date;
    born_date_input.name = worker_data.born_date;
        
    contact_input.value = worker_data.contact;
    contact_input.name = worker_data.contact;

    section_input.value = worker_data.section;
    section_input.name = worker_data.section;

    role_input.value = worker_data.role;
    role_input.name = worker_data.role;

    workload_day_input.value = worker_data.workload_day;
    workload_day_input.name = worker_data.workload_day;

    workload_week_input.value = worker_data.workload_week;
    workload_week_input.name = worker_data.workload_week;

    base_salary_input.value = worker_data.base_salary;
    base_salary_input.name = worker_data.base_salary;
}

// Request worker absences consult and insert results
async function requestAbsencesConsultResults(event, worker_id) {
    // Prevent window reload
    event.preventDefault();

    // Convert data from form to formData object
    const form_data = new FormData(document.getElementById('consult_absences_form'));
    
    // Add the CSRF token directly to form_data
    form_data.append('csrf_token', document.getElementById('csrf_token').value);

    // Add worker id directly to form_data
    form_data.append('id', worker_id);

    // Convert form_data to a JSON object
    const form_object = Object.fromEntries(form_data.entries());

    // Sanitize form data
    form_data.forEach(data => {
        sanitizeInput(data);
    })

    console.log(form_object);

    // Request server to confirm change
    const result = await requestServerAndReturnResponse('/send_absences_consult_results', form_object, json=true);

    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Insert consult results
    document.getElementById('consult_absences_results').innerHTML = result.absences_consult_results;

    // Delete absence button
    const delete_absence_buttons = document.getElementsByName('delete_absence');

    // Ensure that has delete absence buttons and add event listener
    if (delete_absence_buttons) {
         delete_absence_buttons.forEach(button => {
             button.addEventListener('click', async function(event) {
                 await sendAbsenceToDelete(event, worker_id);
             }) 
        })
    }
}


// Request worker absences consult and insert results
async function requestBenefitsConsultResultsAndInsert(event, worker_id) {
    // Prevent window reload
    event.preventDefault();

    // Convert data from form to formData object
    const form_data = new FormData(document.getElementById('consult_benefits_form'));
    
    // Add the CSRF token directly to form_data
    form_data.append('csrf_token', document.getElementById('csrf_token').value);

    // Add worker id directly to form_data
    form_data.append('id', worker_id);

    // Convert form_data to a JSON object
    const form_object = Object.fromEntries(form_data.entries());

    // Sanitize form data
    form_data.forEach(data => {
        sanitizeInput(data);
    })

    console.log(form_object);
    
    // Request server with data to consult and get response
    const result = await requestServerAndReturnResponse('/send_benefits_consult_results', form_object, json=true);

    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }
    
    // Insert consult results
    document.getElementById('consult_benefits_results').innerHTML = result.benefits_consult_results;

    // Delete absence button
    const delete_benefit_buttons = document.getElementsByName('delete_benefit');

    if (delete_benefit_buttons) {
         delete_benefit_buttons.forEach(button => {
             button.addEventListener('click', async function(event) {
                 await sendBenefitToDelete(event, worker_id);
            }) 
        })
    }
}

// Request categories products select by user and insert in popover
async function requestSelectProductsToInventoryForm(event, pagination_index) {
    // Prevent window reload
    event.preventDefault();

    console.log('request_categories');

    // Category filter value
    category_filter = document.getElementById('category').value;

    if (category_filter == 'disabled') {
        sendErrorMessage(event, 'Select a valid category.');
        throw new Error('Select a valid category.', '404');
    }
  
    // Sub categories check options
    const sub_categories_options = document.getElementsByName('sub_category_filter');

    // Sub categories empty array
    let sub_category_filters = [];

    // All sub categories array
    let all_sub_category = [];

    // Get checked sub categories to search
    sub_categories_options.forEach(option => {
        if (option.checked) {
            // Append sub category id to sub_category_filters array
            sub_category_filters.push(option.value);
        }

        // Append sub category value to all sub categories array
        all_sub_category.push(option.value);
    })
    
    // Ensure that has checked boxed
    if (sub_category_filters.length == 0) {
        // If no checked sub categories, search for all
        sub_category_filters = all_sub_category;
    }

    // Data to send
    const data = {
        category_filter: category_filter,
        sub_category_filters: sub_category_filters,
        pagination_index: pagination_index
    }

    await validateForm(event, document.getElementById('create_inventory_form'), '/send_select_products_to_inventory_form', {pagination_index: pagination_index}, form_reset=false);

    // Store products to create inventory
    storageProductsToCreateInvetory();

    // Storaged ids
    const storaged_ids = JSON.parse(sessionStorage.getItem('new_inventory'));

    // Send to inventory check inputs
    const send_to_inventory_check = document.getElementsByName('send_to_inventory');

    if (storaged_ids != null) {
        // Ensure some products is checked already
        send_to_inventory_check.forEach(check => {
            if (storaged_ids.includes(check.id)) {
                // Change check input to checked
                check.checked = true;
            }
        })         
    }
  
    // Change page buttons from pagination navbar
    const change_page_buttons = document.getElementsByName('change_page');

    // Add event listener to change page buttons
    change_page_buttons.forEach(button => {
        button.addEventListener('click', function (event) {
            handlePaginationButtonsAndUpdateResults(event, "inventory_table");
        })
            
    })
    
    // Create inventory button
    const create_inventory_button = document.getElementById('create_inventory');

    // Add event listener to create inventory button
    create_inventory_button.addEventListener('click', async function(event) {
        // Create array with ids already in html
        const products_ids = JSON.parse(sessionStorage.getItem('new_inventory'));

        await sendInventoryToCreate(event, products_ids);
    });
    
}

// Request open_inventories.html and insert in open inventories content
async function requestOpenInventories() {

    // Request server
    const response = await fetch('/render_open_inventories', {method: "POST"});

    const result = await response.json();
    
    // Insert result
    document.getElementById('inventories_action_content').innerHTML = result.open_inventories_html;

    // Check inventory buttons
    const check_inventory_buttons = document.getElementsByName('check_inventory');

    // Add event listeners to check inventory buttons
    check_inventory_buttons.forEach(button => {
        button.addEventListener('click', async function(event) {

            // Inventory id
            let inventory_id = event.target.closest('ul').id;

            requestInventoryInfo(event, inventory_id, 0);
    });
    })

    // Count inventory_buttons
    const count_inventory_buttons = document.getElementsByName('count_inventory');
    
    // Add event listeners to count inventory buttons
    count_inventory_buttons.forEach(button => {
        if (!button.disabled) {
            button.addEventListener('click', async function(event) {
                // Inventory id
                let inventory_id = event.target.closest('ul').id;
                 
                // Request count inventory form
                requestCountInventoryForm(event, inventory_id, 0)
            });
        }
    })

    // Finish inventory buttons
    const finish_inventory_buttons = document.getElementsByName('finish_inventory');

    // Add event listeners to count inventory buttons
    finish_inventory_buttons.forEach(button => {
        if (!button.disabled) {
            button.addEventListener('click', async function(event) {
                // Inventory id
                let inventory_id = event.target.closest('ul').id;

                // Request finish inventory form
                requestFinishInventoryForm(event, inventory_id, 0);

            });
        }
    })

    // Recount inventory buttons
    const recount_inventory_buttons = document.getElementsByName('recount_products');

    // Add event listeners to count inventory buttons
    recount_inventory_buttons.forEach(button => {
        if (!button.disabled) {
            button.addEventListener('click', async function (event) {
                // Get closest inventory id from button clicked
                const inventory_id = event.target.closest('ul').id;

                // Request recount inventory form
                requestRecountInventoryForm(event, inventory_id, 0)
            });
        }
    })

    // Show delete inventory popover buttons
    const show_delete_inventory_buttons = document.getElementsByName('show_pop_over_delete_inventory');

    // Add event listener to show delete inventory popover buttons
    show_delete_inventory_buttons.forEach(button => {
        button.addEventListener('click', async function (event) {
            // Inventory id
            const inventory_id = event.target.closest('ul').id;

            document.getElementById('confirm_submit').value = inventory_id;

            // Show delete confirm pop-over
            showConfirmPopoverAndPersonalize(event, button.value);   
            
        })
    })
}

async function requestInventoryInfo(event, inventory_id, pagination_index,) {
    // Prevent window reload
    event.preventDefault();

    // Data
    const data = {
        inventory_id: inventory_id,
        pagination_index: pagination_index   
    }

    console.log(data);
    // Send request to server and get response
    const result = await requestServerAndReturnResponse('/send_inventory_info', data, json=true);

    // Ensure response has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Insert inventory info in popover content body
    document.querySelector('.pop-over-content-body').innerHTML = result.inventory_info_html;

    // Change popover title
    document.getElementById('edit_title').innerHTML = 'Consult inventory'

    // Add class 'show-pop-over' to popover element
    document.querySelector('.personal-pop-over').classList.add('show-pop-over');

    // Change page buttons from pagination navbar
    const change_page_buttons = document.getElementsByName('change_page');

    // Add event listener to change page buttons
    change_page_buttons.forEach(button => {
        button.addEventListener('click', function (event) {
            handlePaginationButtonsAndUpdateResults(event, "inventory_info", inventory_id);
        })
            
    })

}

// Request inventories consult and insert results
async function requestClosedInventories(event) {
    // Prevent window reload
    event.preventDefault();

    // Date selected to consult
    const date_to_consult = document.getElementById('inventories_dates').value;

    // Send request with date to consult and insert response
    const result = await requestServerAndReturnResponse('/send_closed_inventories_consult_results', date_to_consult);

    // Ensure response has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }
    
    // Insert result in consult inventories content
    document.getElementById('inventories_action_content').innerHTML += result.closed_inventories_consult_results;

    // Check inventory results buttons
    const check_inventory_results_buttons = document.getElementsByName('check_inventory_results');

    // Add event listener to check inventory results buttons
    check_inventory_results_buttons.forEach(button => {
        button.addEventListener('click', async function (event) {
             // Inventory id
            const inventory_id = event.target.closest('ul').id;

            await requestClosedInventoryInfo(event, inventory_id, 0);
        });
    })
}

// Request closed inventories results
async function requestClosedInventoryInfo(event, inventory_id, pagination_index) {
    // Prevent window reload
    event.preventDefault();

    // Inventory data to send
    const inventory_data = {inventory_id: inventory_id, pagination_index: pagination_index};

    // Request server and insert response
    const result = await requestServerAndReturnResponse('/send_closed_inventory_info', inventory_data, json=true);

    // Insert closed inventory results in popover body content
    document.querySelector('.pop-over-content-body').innerHTML = result.closed_inventory_result;
 
    // Add show-pop-over class to popover element
    document.querySelector('.personal-pop-over').classList.add('show-pop-over');
 
    // Change popover title
    document.getElementById('edit_title').innerHTML = 'Inventory results'

    // Change page buttons from pagination navbar
    const change_page_buttons = document.getElementsByName('change_page');

    // Add event listener to change page buttons
    change_page_buttons.forEach(button => {
        button.addEventListener('click', function (event) {
            handlePaginationButtonsAndUpdateResults(event, "closed_inventory", inventory_id);
        })            
    }) 
}

// Request products and/or services searched with filters and insert result
async function requestMyProductsAndServiceSearchFilters(event, pagination_index) {
    // Prevent window reload
    event.preventDefault();

    let form_data = new FormData(document.getElementById('search_products_and_services'));

    form_data.append('pagination_index', pagination_index);

    // Convert form_data to a JSON object
    const form_object = Object.fromEntries(form_data.entries());

    console.log(form_object);

    const result = await requestServerAndReturnResponse('/search_my_products_and_services', form_object, json=true);

    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }
      
    // Insert results
    showPopOver(result.rendered_search, "Search results");

     // Change page buttons from pagination navbar
     const change_page_buttons = document.getElementsByName('change_page');

     // Add event listener to change page buttons
     change_page_buttons.forEach(button => {
         button.addEventListener('click', function (event) {
             handlePaginationButtonsAndUpdateResults(event, "my_products_search");
         })            
     })
}

// Request products without sales in last 15 days
async function requestProductsWithoutSalesInfo(event, pagination_index) {
    // Prevent window reload
    event.preventDefault();

    // Send request for products without sales in last 15 days with pagination index
    const result = await requestServerAndReturnResponse('/send_products_without_sales_info', pagination_index);

    // Ensure response has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Remove class display-none from personal-pop-over element
    document.querySelector('.personal-pop-over').classList.add('show-pop-over');

    // Change pop-over title
    document.getElementById('edit_title').innerHTML = 'Products without sales in last 15 days'

    // Insert template rendered result in popover element
    document.querySelector('.pop-over-content-body').innerHTML = result.products_without_sales_html; 

    // Change page buttons from pagination navbar
    const change_page_buttons = document.getElementsByName('change_page');

    // Add event listener to change page buttons
    change_page_buttons.forEach(button => {
        button.addEventListener('click', function (event) {
            handlePaginationButtonsAndUpdateResults(event, "without_sales_info");
        })            
    }) 
}

// Request products without sales in last 15 days and with null and negative stock
async function requestProductsIndexStockInfo(event, pagination_index, search_type) {
    // Prevent window reload
    event.preventDefault();

    // Data to send
    const data_to_send = {pagination_index: pagination_index, search_type: search_type};

    // Send request for products without sales in last 15 days with pagination index
    const result = await requestServerAndReturnResponse('/send_products_stock_info', data_to_send, json=true);

    // Ensure response has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Remove class display-none from personal-pop-over element
    document.querySelector('.personal-pop-over').classList.add('show-pop-over');

    let title;

    if (search_type == 'null_stock') {
        title = 'Products with null stock'
    }
    else {
        title = 'Products with negative stock'
    }

    // Change pop-over title
    document.getElementById('edit_title').innerHTML = title;

    // Insert template rendered result in popover element
    document.querySelector('.pop-over-content-body').innerHTML = result.products_stock_info_html; 

    // Change page buttons from pagination navbar
    const change_page_buttons = document.getElementsByName('change_page');

    // Add event listener to change page buttons
    change_page_buttons.forEach(button => {
        button.addEventListener('click', function (event) {
            handlePaginationButtonsAndUpdateResults(event, search_type);
        })            
    })


}

// Request mensal report selected by user
async function requestMensalReport(event, date_selected) {
    // Prevent window reload
    event.preventDefault();

    // Request server for mensal report with date selected
    const result = await requestServerAndReturnResponse('/send_mensal_report', date_selected);

    // Insert content in popover
    showPopOver(result.mensal_report_result_html, `Mensal report ${date_selected}`);
}

// Request POS with reader mode select by user
async function requestPOS(event, bar_code_reader_mode) {
    // Prevent window reload
    event.preventDefault();

    // Clean localStorage
    localStorage.removeItem('pos_registry');

    // Request POS content
    const result = await requestServerAndReturnResponse('/pos', bar_code_reader_mode);

    // Insert response pos_html
    document.getElementById('index_body').innerHTML = result.pos_html;

    // Insert product or service bar code input element
    var insert_bar_code_input = document.getElementById('insert_product_or_service');

    console.log(bar_code_reader_mode);

    // Ensure which mode user selected
    if (bar_code_reader_mode == 'manual_mode') {
        // Add click event listener to insert bar code input
        insert_bar_code_input.addEventListener('input', async function (event) {
            // Request product or service information and autocomplete
            await requestProductOrServiceAutoComplete(event, 'pos_registry_product_or_service');
        })

        // Button to insert bar code
        const insert_bar_code_button = document.getElementById('insert_bar_code');

        // Add event listener to insert bar code button
        insert_bar_code_button.addEventListener('click', async function(event) {

            await validatePOSregistry(event);
        })
    }
    else {
        // Add input event listener to insert bar code input
        insert_bar_code_input.addEventListener('input', async function (event) {
            // Get bar code inputed by user
            const bar_code = event.target.value;

            // Request product or service information with bar code readed
            const result = await requestServerAndReturnResponse('/send_pos_scanned_product', bar_code);

            // Get info sended by server
            const bar_code_info_queried = result.bar_code_info_queried[0];

            console.log(bar_code_info_queried);

            // Create a localStorage with pos registry info
            localStorage.setItem('pos_registry', JSON.stringify([{id: bar_code_info_queried.id, sell_price: bar_code_info_queried.sell_price, unity_m: bar_code_info_queried.unity_m, type: bar_code_info_queried.type}]));
            
            console.log(localStorage.getItem('pos_registry'));

            await validatePOSregistry(event);

        })   
    }
    
    // Autofocus input dinamically
    insert_bar_code_input.focus();

    // POS calculate buttons
    const calculate_buttons = Array.from(document.getElementsByName('numbers_and_multiply'));

    // Registry info h5 element
    var registry_info = document.getElementById('registry_info');

    // Bar code info h5 element
    var bar_code_info = document.getElementById('bar_code');

    // Add event listener to calculate buttons
    calculate_buttons.forEach(button => {
        button.addEventListener('click', function() {

            console.log(button.id)
            console.log(registry_info.innerHTML.slice(0, 1));

            // Clean registry_info.innerHTML
            if (button.id == 'clean_registry') {
                
                registry_info.innerHTML = '';
                bar_code_info.innerHTML = '';
            }
            // If registry_info.innerHTML is empty, if user click multiply button send error message with instructions else set update registry_info.innerHTML to button innerHTML
            else if (registry_info.innerHTML == '') {
                if (button.id == 'multiply_registry' || button.value == '.') {
                    
                    // Errors
                    const error_message = 'First select units, click button to multiply and insert description or bar code!';
                    const html_error = '<h5 class="color-black">First select <span class="personal-blue-color">units</span>, click <span class="personal-blue-color">"x"</span> button to <span class="personal-blue-color">multiply</span> and insert <span class="personal-blue-color">description</span> or <span class="personal-blue-color">bar code</span>!</h5>'

                    // Send Pos error message
                    sendPosErrorMessage(error_message, html_error);

                }
                else {
                    registry_info.innerHTML = button.innerHTML;
                } 
            }        
            // Ensure after a multiply sign user insert bar code else send error message with instructions
            else if (registry_info.innerHTML.slice(-1) === 'x') {
                if (button.id == 'multiply_registry' || button.value == 'numeric') {

                    // Errors
                    const error_message = 'Insert description or bar code!';
                    const html_error = 'Insert <span class="personal-blue-color">description</span> or <span class="personal-blue-color">bar code</span>!</h5>' 
                    
                    // Send Pos error message
                    sendPosErrorMessage(error_message, html_error);

                }
            }
            // Ensure after a dot user click in a numeric button
            else if (registry_info.innerHTML.slice(-1) === '.'){
                if (button.value == 'numeric') {
                    registry_info.innerHTML += button.innerHTML;
                } 
            }
            // Ensure that exists only one dot in registry_info.innerHTML and increment registry_info.innerHTML with button.innerHTML 
            else {
                if (registry_info.innerHTML.indexOf('.') == -1) {
                    if (button.value == 'numeric' || button.value == '.') {
                        registry_info.innerHTML += button.innerHTML;
                        }     
                }  
                else {
                    if (button.value == 'numeric') {
                    
                        // Get index of '.'
                        const dot_index = registry_info.innerHTML.indexOf('.');
                            
                        // Ensure length after dot is not higher tha1%+n 3
                        if (registry_info.innerHTML.slice(dot_index, -1).length < 3) {
                            registry_info.innerHTML += button.innerHTML;
                        }
                    }
                }

                // If button clicked is 'x' insert space + 'x'
                if (button.id == 'multiply_registry') {
                    registry_info.innerHTML += (' ' + button.innerHTML);
                }   
            }
        })
    })

    // Delete last registry button
    const delete_last_registry_button = document.getElementById('delete_last_registry');

    // Add event listener to delete last registry button
    delete_last_registry_button.addEventListener('click', async function(event) {
        // Send request to delete POS registry
        await deletePosRegistry(event, -1);

        // Send request to update POS purchase info
        await requestPosPurchaseInfo(event);
    })

    // Select registry to delete button
    const select_registry_to_delete_button = document.getElementById('delete_registry');

    // Set registry index to 0
    let index = 0

    // Add event listener to delete last registry button
    select_registry_to_delete_button.addEventListener('click', async function(event) {
        // Remove 'display-none' class from all butons with name 'delete_registry'
        document.getElementsByName('delete_registry').forEach(button => {
            button.classList.remove('display-none');

            button.addEventListener('click', async function (event) {
                // Send request to delete POS registry
                await deletePosRegistry(event, index);

                // Send request to update POS purchase info
                await requestPosPurchaseInfo(event);
            })
        })
    })

    // Copy last registry button
    const copy_last_registry_button = document.getElementById('copy_registry');

    // Add event listener to copy last registry button
    copy_last_registry_button.addEventListener('click', async function(event) {
        // Send request to copy last registry and update purchase
        await copyPosLastRegistry(event);

        // Send request to update request purchase info
        await requestPosPurchaseInfo(event);
    })

    // Payment button
    const payment_button = document.getElementById('payment');

    // Add event listener to payment button
    payment_button.addEventListener('click', async function(event) {
        await requestPaymentMenu(event);
    });

    // Refund sale button
    const refund_sale_button = document.getElementById('refund_sale');

    // Add event listener to refund sale button
    refund_sale_button.addEventListener('click', async function(event) {
        await requestRefundSaleMenu(event, 0);
    })
}


// Request refund sale menu
async function requestRefundSaleMenu(event, pagination_index) {
    // Prevent window reload
    event.preventDefault();

    // Request server
    const result = await requestServerAndReturnResponse('/send_pos_refund_sale_menu', pagination_index);

    // Ensure request has no errors
    if (result.errorData) {
        // Send POS error message
        sendPosErrorMessage(result.errorData.error, result.errorData.error);
        
    };

    // Show pop over with payment menu
    showPopOver(result.pos_refund_sale_menu_html, "Refund sale menu");

    console.log(document.querySelectorAll('.sale_information'));

    // Add event listener to sales table rows
    document.querySelectorAll('.sale_information').forEach(row => {
        row.addEventListener('click', async function(event) {
            await requestPosSaleInfo(event, row.id);
        });
    })

    // Change page buttons from pagination navbar
    const change_page_buttons = document.getElementsByName('change_page');

    // Add event listener to change page buttons
    change_page_buttons.forEach(button => {
        button.addEventListener('click', function (event) {
            handlePaginationButtonsAndUpdateResults(event, "sale_info");
        })
    })
}

// Request POS sale info
async function requestPosSaleInfo(event, row_id) {
    // Prevent window reload
    event.preventDefault();

    // Request server for sale info with sale id
    const result = await requestServerAndReturnResponse('/send_pos_sale_info_to_refund', row_id);

    // Ensure request has no errors
    if (result.errorData) {
        // Send error message
        sendPosErrorMessage(result.errorData.error, result.errorData.error);

        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Show pop over with sale info
    showPopOver(result.sale_info_to_refund_html, "Refund sale")

    // Select units select elements
    const select_units_elements = document.getElementsByName('select_units');

    // Add event listener to refund selected products button
    document.getElementById('refund_selected_products').addEventListener('click', async function(event) {
        // Refund selected products menu buttons div element
        var refund_products_menu_content = document.getElementById('refund_selected_products_menu');

        // Remove 'display-none' class from div element that contains option buttons to refund selected products
        refund_products_menu_content.classList.remove('display-none');

        // Refund main buttons menu content
        var refund_main_options_content = document.getElementById('refund_options');

        // Add 'display-none' class to div element that contains main buttons
        refund_main_options_content.classList.add('display-none');

        // Remove 'display-none' class from select elements to select units to refund
        select_units_elements.forEach(select => {
            select.classList.remove('display-none');
        })

        // Add event listener to confirm products to refund
        document.getElementById('confirm_products_to_refund').addEventListener('click', async function(event) {

            // Products id and units to refund empty array
            const ids_and_units = [];

            // Itherate select units select elements
            select_units_elements.forEach(select => {
                // Append products with selected value higher than 0
                if (select.value != 0) {
                    ids_and_units.push({id: select.id, units: select.value});
                }
            })

            // Ensure user selected products
            if (ids_and_units.length == 0) {
                // Send error message
                sendErrorMessage(event, 'Please select products to refund!')
            }
            else {
                // Request server to refund products selected
                await sendSaleSelectedProductsToRefund(event, ids_and_units, row_id);
            }
        })
        // Add event listener to cancel products to refund
        document.getElementById('cancel').addEventListener('click', function () {

            // Get back original pos sale info
            requestPosSaleInfo(event, row_id);
        })
    })

    // Add event listener to refund entire sale button
    document.getElementById('refund_entire_sale').addEventListener('click', async function(event) {
        // Request server to refund entire sale
        sendSaleToRefund(event, row_id);
    })

}

// Request POS purchase info
async function requestPosPurchaseInfo(event) {
    // Prevent window reload
    event.preventDefault();

    // Send request to server
    const response = await fetch('/send_pos_purchase_info_rendered');

    const result = await response.json();

    document.getElementById('purchase_info').innerHTML = result.pos_purchase_info_html;

}

// Request index main info if user is logged
async function requestIndexMainInfo() {
    // Send request
    const response = await fetch('/send_index_main_info', {method: 'POST'});
    
    // Response result
    const result = await response.json();

    // Remove tooltip from old index to dont bug with other tooltips
    if (document.querySelector('.tooltip')) {
        document.querySelector('.tooltip').remove();
    }

    // Insert index_main_info_html in box_content element
    document.getElementById('index_main_content').innerHTML = result.index_main_info_html;

    // Button that show products without sales in last 15 days info
    const show_products_without_sales = document.getElementById('show_products_without_sales_info');

    // Button that show products with null or 0 stock
    const show_products_with_null_stock = document.getElementById('show_products_with_null_stock_info');

    // Button that show products with negative stocks
    const show_products_with_negative_stock = document.getElementById('show_products_with_negative_stock_info');

    // Ensure buttons exist and set event listeners
    if (show_products_without_sales) {
        show_products_without_sales.addEventListener('click', async function (event) {
            // Prevent window reload
            event.preventDefault();

            // Request products without sales in last 15 days info
            await requestProductsWithoutSalesInfo(event, 0);
        });
    }

    if (show_products_with_null_stock) {
        show_products_with_null_stock.addEventListener('click', async function(event) {
            // Prevent window reload
            event.preventDefault();

            // Request products with null stock
            await requestProductsIndexStockInfo(event, 0, "null_stock");
        })
    }

    if (show_products_with_negative_stock) {
        show_products_with_negative_stock.addEventListener('click', async function(event) {
            // Prevent window reload
            event.preventDefault();

            // Request products with negative stock
            await requestProductsIndexStockInfo(event, 0, "negative_stock");
        })
    }

    // Get number of products registered
    const number_of_products_registered = Number(document.getElementById('products_registered').innerHTML);

    // Button to open store
    const open_store_button = document.getElementById('open_store');

    if (open_store_button && number_of_products_registered > 0) {
        // Add event listener to open store button
        open_store_button.addEventListener('click', openStore);
    }
    
    // Button to close store
    const close_store_button = document.getElementById('close_store');
    
    if (close_store_button) {
        // Add event listener to close store button
        close_store_button.addEventListener('click', async function (event) {
           await showConfirmPopoverAndPersonalize(event, 'close_day');
        });
    }

    // Button to start monitoring sales and clients
    const start_monitoring_button = document.getElementById('start_monitoring');

    if (start_monitoring_button) {
        start_monitoring_button.addEventListener('click', startMonitoringSalesAndClients);
    }

    // Button to stop monitoring sales and clients
    const stop_monitoring_button = document.getElementById('stop_monitoring');

    if (stop_monitoring_button) {
        stop_monitoring_button.addEventListener('click', stopMonitoringSalesAndClients);
    }

    // Button to start POS
    const start_pos = document.getElementById('start_pos');

    if (start_pos) {
        start_pos.addEventListener('click', startPOS);
    }

    // Allow Boostrapp Tooltips
    allowToolTips();
}

// Request open session store POS sales and clients
async function requestActualPosSalesAndClients(event) {
    // Prevent window reload
    event.preventDefault();

    // Request server for actual sales and clients
    const response = await fetch('/send_pos_sales_and_clients', {method: "POST"});

    const result = await response.json();

    document.getElementById('sales').innerHTML = result.sales_and_clients.sales;
    document.getElementById('clients').innerHTML = result.sales_and_clients.clients;

}

// Request POS purchase info
async function requestPosPurchaseInfo(event) {
    // Prevent window reload
    event.preventDefault();

    // Send request to server
    const response = await fetch('/send_pos_purchase_info_rendered');

    const result = await response.json();

    document.getElementById('purchase_info').innerHTML = result.pos_purchase_info_html;

}


async function requestAuthenticatorOptions(setting_to_change) {
    // Request authenticator_options.html
    const result = await requestServerAndReturnResponse('/send_authenticator_options');

    // Insert authenticator_options.html in popover and show
    showPopOver(result.authenticator_options, "Authenticator");

    // Add event listener to password button
    document.getElementById('authenticate_password').addEventListener('click', async function() {
        await requestAuthenticatePasswordForm(setting_to_change)
    });
    
    // Add event listener to personal code button
    document.getElementById('authenticate_personal_code').addEventListener('click', async function() {
        await requestAuthenticatePersonalCodeForm(setting_to_change)
    });
    
}

async function requestAuthenticatePasswordForm(setting_to_change) {
    // Request change company name form
    const result = await requestServerAndReturnResponse('/send_authenticate_password_form');
    
    showPopOver(result.authenticate_password_form, 'Authenticate password');

    // Add event listener to confirm change company name
    document.getElementById('confirm').addEventListener('click', async function(event) {
        // Prevent window reload
        event.preventDefault();

        // Get form element
        const authenticate_password_form_element = document.getElementById('authenticate_password_form');

        // Request server to validate form
        await authenticateForm(event, authenticate_password_form_element, 'password', setting_to_change);

    })
}

async function requestAuthenticatePersonalCodeForm(setting_to_change) {
    // Request change company name form
    const result = await requestServerAndReturnResponse('/send_authenticate_personal_code_form');
    
    showPopOver(result.authenticate_personal_code_form, 'Authenticate personal code');

    handlePersonalCodeInput();

    // Add event listener to confirm change company name
    document.getElementById('confirm').addEventListener('click', async function(event) {
        // Prevent window reload
        event.preventDefault();

        // Get form element
        const authenticate_personal_code_form_element = document.getElementById('authenticate_personal_code_form');

        // Request server to validate form
        await authenticateForm(event, authenticate_personal_code_form_element, 'personal_code', setting_to_change);
    })    

}

// Request purchase payment menu
async function requestPaymentMenu(event) {
    // Prevent window reload
    event.preventDefault();
    
    // Request server
    const response = await fetch('/send_pos_payment_menu', {method: "POST"});

    if (!response.ok) {

        const errorData = await response.json();

        sendPosErrorMessage(errorData.error, errorData.error);
        
    };

    // Get response
    const result = await response.json()

    // Show pop over with payment menu
    showPopOver(result.pos_payment_menu_html, "Payment menu");

    // Add event listener to cash payment option
    document.getElementById('cash').addEventListener('click', async function(event) {
        // Cash input element
        const cash_input_value = document.getElementById('cash_value').value;

        await sendSaleToRegister(event, cash_input_value, 'cash');

        await requestPosPurchaseInfo(event);
    })

    // Add event listener to bank payment option
    document.getElementById('atm').addEventListener('click', async function(event) {

        await sendSaleToRegister(event, '', 'atm');

        await requestPosPurchaseInfo(event);
    });
}

async function sendProductToValidateAndInsertinTempOrderList(event, product_id) {
    // Prevent window from reload
    event.preventDefault();

    await validateForm(event, document.getElementById('register_product_in_order'), '/validate_product_and_insert_in_temp_order_list', product_id);

    // Request order table and update
    await requestOrderTableAndUpdate(0);
}

async function sendProductAndDeleteFromOrderList(event) {
    // Prevent window reload
    event.preventDefault();

    // Get product id
    let product_id = event.target.closest('tr').id;

    // Request server with product description to delete and return response
    const result = await requestServerAndReturnResponse('/delete_product_from_order_list', sanitizeInput(product_id));
    
    // Ensure theres no errors or response sucessfull
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Send sucess message
    sendSucessMessage(event, result.sucess_message);

    // Request order table and update
    await requestOrderTableAndUpdate(0);
}

async function sendProductToValidateRegister (event) {

    // Prevent window reload
    event.preventDefault();

    await validateForm(event, document.getElementById('register_product_form'), '/validate_product_register');

    // Get product list length element
    const product_list_length_element = document.getElementById('product_list_len');

    // Get product list len length
    let product_list_length = product_list_length_element.innerHTML;


    // Reset form
    const form = document.querySelector('form');
    form.reset();
    
    // Update products list len
    if (product_list_length == '') {
        product_list_length_element.innerHTML = 1;
    }
    else {
        // Convert product_list_len html to integer
        product_list_length = parseInt(product_list_length);     
        product_list_length_element.innerHTML = product_list_length + 1;
    }
}

// Send request with product description and remove from register list
async function sendProductToRemoveFromRegisterList(event) {
    // Prevent page from reload
    event.preventDefault();

    // Get product description closest to remove button
    const closest_table_row = event.target.closest('tr')
    const closest_description = closest_table_row.querySelector('.row_description').innerHTML;
    
    // Send request with product description to remove
    const result = await requestServerAndReturnResponse('/remove_product_from_register_list', sanitizeInput(closest_description));

    // Ensure response result has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error, popover=true);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Send sucess message
    sendSucessMessage(event, result.sucess_message);
    
    // Remove row
    closest_table_row.remove();

    // Result element
    const result_element = document.querySelector('.result');

    let number_of_products = result_element.innerHTML;

    result_element.innerHTML = parseInt(number_of_products) - 1;

    // Update products list len and results element
    if (product_list_length == 1) {
        product_list_length_element.innerHTML = '';
        result_element.innerHTML = 0;
    }
    else {
        // Convert product_list_len html to integer
        product_list_length = parseInt(product_list_length);     
        product_list_length_element.innerHTML = product_list_length - 1;
        result_element.innerHTML = product_list_length - 1;
    }

    // Ensure list is not empty, else disable register products and remove all products buttons
    if (product_list_length_element.innerHTML == '') {
        // Disable remove all products button and register button 
        document.getElementById('confirm_remove_all_products_from_register_list').disabled = true;  
        document.getElementById('confirm_register_products').disabled = true;     
    }

}

// Send product to edit and insert sucess html
async function sendProductToEdit(product_id, event) {
    // Prevent window reload
    event.preventDefault();

    console.log(product_id);

    await validateForm(event, document.getElementById('edit_product_form'), '/validate_and_edit_product', product_id);

    // Search to edit button menu button
    const search_button = document.getElementById('submit_search_and_edit');

    // Simulate event click in home button
    const clickEvent = new MouseEvent('click', {
       view: window,
       bubbles: true,
       cancelable: true
   });

   search_button.dispatchEvent(clickEvent);
}


// Send request with product to delete
async function sendProductToDelete(event, product_id) {
    // Prevent window from reload
    event.preventDefault();

    // Send request with product internal code
    const result = await requestServerAndReturnResponse('/delete_product', product_id);

    // Ensure request has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error, popover=true);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    showPopOver(result.delete_product_sucess_html, 'Product deleted')

    // Simulate search product or service button click event to update searchs
    const clickEvent = new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: true
    });

    document.getElementById('submit_search_and_edit').dispatchEvent(clickEvent);

}

// Send request with service id, validate and edit service
async function sendServiceToEdit(service_id, event) {
    // Prevent window reload
    event.preventDefault();

    // Get service calculated cost price
    const service_calculated_cost_price = parseInt(document.getElementById('calculated_cost_price').innerHTML);

    console.log(service_calculated_cost_price);

    const input_cost_price_value = document.getElementById('cost_price').value;

    // Ensure input_cost_price_value is higher or equal than service_calculated_cost_price
    if (service_calculated_cost_price > input_cost_price_value) {
        sendErrorMessage(event, 'Service cost price must be equal or higher than calculated service cost price.')
        throw new Error('Service cost price must be equal or higher than calculated service cost price.', '404');
    }
    // Send form data to validate
    await validateForm(event, document.getElementById('service_form'), '/validate_and_edit_service', service_id);

    // Search to edit button menu button
    const search_button = document.getElementById('submit_search_and_edit');

    // Simulate event click in home button
    const clickEvent = new MouseEvent('click', {
       view: window,
       bubbles: true,
       cancelable: true
   });

   search_button.dispatchEvent(clickEvent);

}

// Send service id in request to delete service
async function sendServiceToDelete(service_id, event) {
    // Prevent window from reload
    event.preventDefault();

    // Send request with product internal code
    const result = await requestServerAndReturnResponse('/delete_service', sanitizeInput(service_id));

    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error, popover=true);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    showPopOver(result.delete_service_sucess_html, 'Success!');

    // Simulate search product or service button click event to update searchs
    const clickEvent = new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: true
    });

    document.getElementById('submit_search_and_edit').dispatchEvent(clickEvent);
}

// Send uploaded order data and validate
async function sendUploadedOrderAndValidate(event) {
    // Prevent window reload
    event.preventDefault();

    // Get file input
    const file_input = event.target.closest('input');
    const file = file_input.files[0];

    // Create object FromData
    formData = new FormData();

    // Append file and token
    formData.append('file', file);

    // Send request with uploaded 'csv' file and return response
    const result = await requestServerAndReturnResponse('validate_order_upload', formData);

    // Ensure theres no errors or response sucessfull
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);

        // Reset upload input
        event.target.value = '';
        event.target.addEventListener('input', sendUploadedOrderAndValidate);

        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
        
    }

    if (result.order_data) {
        // Uploaded order data
        const order_data = result.order_data;

        // Errors from order
        let order_errors = '';
        let errors = 0;

        // Validata data and insert in temp_order_list
        for (let i = 0; i < order_data.length; i++) {

            // Send request to validate products and insert in temp_order_list table
            const result = await requestServerAndReturnResponse('/validate_product_and_insert_in_temp_order_list', order_data[i], json=true);

            if (result.errorData) {
                // Incremenet error to order_errors
                order_errors += `<div class='col-lg-12 mb-1 mt-1'>Error -> Row ${i + 1}: ${result.errorData.error}</div>`;
                errors++;
            }
        }

        if (errors > 0) {
            // Send errors
            sendErrorMessage(event, order_errors);

            // Delete all products from order list
            await removeAllProductsFromOrderList(event);

        }
        else {
            // Request order table and update
            await requestOrderTableAndUpdate(0);
            
            // Send sucess message
            sendSucessMessage(event, result.sucess_message);
        }

        // Reset upload input
        event.target.value = '';
        event.target.addEventListener('input', sendUploadedOrderAndValidate);   
    }
}

// Send request with expense, validate and insert
async function sendExpenseToInsert(event) {
    // Prevent window reload
    event.preventDefault();

    // Validate expense fokrm
    await validateForm(event, document.getElementById('register_expense_form'), 'validate_and_register_expense');

    simulateClickEvent(document.getElementById('expenses'));
    
}

// Send request with expense id to delete
async function sendExpenseToDelete(event) {
    // Prevent window reload
    event.preventDefault();

    // Delete expense id
    const deleted_expense_id = event.target.closest('.expense').id;

    // Request server with expense id to delete and get response
    const result = await requestServerAndReturnResponse('/delete_expense', sanitizeInput(deleted_expense_id));

    // Send sucess message
    sendSucessMessage(event, result.sucess_message);

    // Check button
    const check_button = document.getElementById('check_expense');

    // Simulate event click in check button to update result
    const clickEvent = new MouseEvent('click', {
       view: window,
       bubbles: true,
       cancelable: true
   });

   check_button.dispatchEvent(clickEvent);

}

// Send request with worker data to validate and insert
async function sendWorkerToValidate(event, register=false, edit=false) {
    // Prevent window reload
    event.preventDefault();
    
    let form_data;

    if (edit) {
        // Convert data from form to formData object
        form_data = new FormData(document.getElementById('edit_worker_form'));

        // Worker number
        const worker_id = document.getElementById('worker_id').value;

        // Append to form data worker id
        form_data.append('id', worker_id);
    }
    else if (register) {

        // Convert data from form to formData object
        form_data = new FormData(document.getElementById('register_worker_form'));
    }

    // Add the CSRF token directly to form_data
    form_data.append('csrf_token', document.getElementById('csrf_token').value);


    // Sanitize form data
    form_data.forEach(data => {
        sanitizeInput(data);
    })


    // Convert form_data to a JSON object
    const form_object = Object.fromEntries(form_data.entries());

    console.log(form_object);

    // Send request with worker data
    const result = await requestServerAndReturnResponse('/validate_worker', form_object, json=true);

    console.log(result.cleaned_data);

    // Ensure request has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }
    
    // Register worker
    if (register) {
        await registerWorker(event, result.cleaned_data);

        // Rest form
        const form = event.target.closest('form');
        form.reset();

    }
    // Edit worker
    if (edit) {
        
        await sendWorkerDataToUpdate(event, result.cleaned_data);
    }
}

// Send request with worker data to validate
async function sendWorkerDataToUpdate(event, worker_data) {
    // Prevent window reload
    event.preventDefault();

    console.log("Send to update..")
    console.log(worker_data);

    const result = await requestServerAndReturnResponse('/update_worker_data', worker_data, json=true);

    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Send sucess message
    document.querySelector('.pop-over-content-body').innerHTML = `<span class="sucess-message f-bold">${result.sucess_message}</span>`;

}

// Send request with absence to validate and register
async function sendAbsenceToValidateAndRegister(event, worker_id) {
    // Prevent window reload
    event.preventDefault();

    console.log(event.target.id);

    // Validate absence data
    await validateForm(event, document.getElementById('register_absence_form'), '/validate_and_register_absence', worker_id);

}

// Send worker to delete
async function sendWorkerToDelete(event) {
    // Prevent window reload
    event.preventDefault();

    // Worker number
    const worker_id = document.getElementById('worker_id').innerHTML;

    const result = await requestServerAndReturnResponse('/delete_worker', sanitizeInput(worker_id));

     // Ensure response result has no errors
     if (result.errorData) {
        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Send sucess message
    showPopOver(`<span class="sucess-message f-bold">${result.sucess_message}</span>`, 'Workers');

}

// Send absence to delete
async function sendAbsenceToDelete(event, worker_id) {
    // Prevent window reload
    event.preventDefault();

    // Clicked delete button row
    const row = event.target.closest('tr');
    
    // Row dates
    const start_date = row.querySelector('.row_start_date').innerHTML;

    // Absence data
    const absence_info = {worker_id: sanitizeInput(worker_id), 
                          start_date: sanitizeInput(start_date)};
    
    // Response result                   
    const result = await requestServerAndReturnResponse('/delete_absence', absence_info, json=true);

    // Ensure response result has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Send response result sucess message
    showPopOver(result.success_response, 'Absences');
}

// Send request with worker benefit to validate and register
async function sendBenefitToValidateAndRegister(event, worker_id) {
    // Prevent window reload
    event.preventDefault();

    // Absence start date
    const benefit = document.getElementById('benefit').value;

    await validateForm(event, document.getElementById('register_benefit_form'), '/validate_and_register_benefit', worker_id);
    
    // Consult abscences content
    const consult_benefits_content = document.getElementById('consult_benefits_results').innerHTML;

    // Simulate click event
    const clickEvent = new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: true
    });

    // Ensure consult abscences content is not empty
    if (consult_benefits_content == '') {
        // Show benefits form button
        const show_benefit_form_button = document.getElementById('show_benefits_form');
        
        // Simulate event in show absence form button
        show_benefit_form_button.dispatchEvent(clickEvent);

    }
    else {
        // Consult absences button
        const consult_benefits_button = document.getElementById('consult_benefits');

        // Simulate event in consult abscence button
        consult_benefits_button.dispatchEvent(clickEvent);
    }
}

// Send request with inventory to create
async function sendInventoryToCreate(event, products_ids)  {
    // Prevent window reload
    event.preventDefault();

    // Send request with products_id_array and get response
    const result = await requestServerAndReturnResponse('/create_inventory', products_ids, json=true);
    
    // Ensure response result has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Insert sucess message
    document.querySelector('.pop-over-content-body').innerHTML = result.sucess_message;

}

// Send request with worker id and benefit id to delete
async function sendBenefitToDelete(event, worker_id) {
    // Prevent window reload
    event.preventDefault();

    // Clicked delete button row
    const row = event.target.closest('tr');

    // Benefit id
    const benefit_id = row.id;

    // Benefit data
    const benefit_data = {worker_id: sanitizeInput(worker_id),
                          benefit_id: sanitizeInput(benefit_id)
    }
    
    // Response result                   
    const result = await requestServerAndReturnResponse('/delete_benefit', benefit_data, json=true);

    // Ensure response result has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Send response result sucess message
    showPopOver(result.sucess_message, 'Benefits');

}

// Send request with inventory counts and inventory id
async function sendInventoryCounts(event, inventory_id) {
    // Prevent window reload
    event.preventDefault();

    // Get session storage values
    const counts = JSON.parse(sessionStorage.getItem(inventory_id));

    const data = {inventory_id: sanitizeInput(inventory_id), counts: counts};

    console.log(data);

    // Request server with ids_and_counts array and get response
    const result = await requestServerAndReturnResponse('/register_inventory_counts', data, json=true);

    // Ensure response result has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Insert sucess html
    document.querySelector('.pop-over-content-body').innerHTML = result.sucess_html;

    // Clean session storage
    sessionStorage.removeItem(inventory_id);

    // Request and update open inventories
    requestOpenInventories();
}

// Send inventory recounts
async function sendInventoryRecounts(event, inventory_id) {
    // Prevent window reload
    event.preventDefault();

    // Get session storage values
    const counts = JSON.parse(sessionStorage.getItem(inventory_id));

    // Data to send 
    const data = {inventory_id: sanitizeInput(inventory_id), counts: counts};

    // Request server with ids_and_counts array and get response
    const result = await requestServerAndReturnResponse('/register_inventory_counts', data, json=true);

    // Ensure response result has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Insert sucess html
    document.querySelector('.pop-over-content-body').innerHTML = result.sucess_html;

    // Clean session storage
    sessionStorage.removeItem(inventory_id);

    // Update open inventories contentx
    requestOpenInventories();

}

// Send request with products to recount
async function sendProductsToRecountInventory(event, inventory_id) {
    // Prevent window reload
    event.preventDefault();

    // Get session storage values
    const products_ids = JSON.parse(sessionStorage.getItem(inventory_id));

    // Data to send 
    const data = {inventory_id: inventory_id, products_ids: products_ids};

    // Request server and get response 
    const result = await requestServerAndReturnResponse('/send_products_to_recount', data, json=true);

    // Insert sucess message
    document.querySelector('.pop-over-content-body').innerHTML = result.sucess_html;

    // Update open inventories
    requestOpenInventories();

    // Clean session storage
    sessionStorage.removeItem(inventory_id);

}

// Send request with inventory id to finish
async function sendInventoryToFinish(event, inventory_id) {
    // Prevent window reload
    event.preventDefault();

    // Request server with inventory id and get response
    const result = await requestServerAndReturnResponse('/register_finish_inventory', inventory_id);

    // Ensure response result has no errors
    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Insert count_inventory_form_html in popover body content
    document.querySelector('.pop-over-content-body').innerHTML = result.sucess_html;

    // Update open inventories content
    requestOpenInventories();
}

// Send inventory to delete
async function sendInventoryToDelete(event, inventory_id) {
    // Prevent window reload
    event.preventDefault();

    console.log(inventory_id);
    
    // Request server and get response
    const result = await requestServerAndReturnResponse('/delete_inventory', inventory_id);
  
    // Ensure response has no errors
    if (result.errorData) {
  
         sendErrorMessage(event, result.errorData.error);
         throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }
    
    // Confirm popover element
    const confirm_pop_over = document.querySelector('.confirm-pop-over');

    // Remove class 'show-pop-over' from confirm-pop-over
    confirm_pop_over.classList.remove('show-pop-over');

    // Main pop-over
    const main_pop_over = document.querySelector('.personal-pop-over');

    // Add 'show-pop-over' class to main_pop_over
    main_pop_over.classList.add('show-pop-over');

    // Insert count_inventory_form_html in main popover body content
    main_pop_over.querySelector('.pop-over-content-body').innerHTML = result.sucess_html;

    // Update open inventories content
    requestOpenInventories();
}

// Request server to refund products selected
async function sendSaleSelectedProductsToRefund(event, ids_and_units, sale_id) {
    // Prevent window reload
    event.preventDefault();

    // Request server with product ids and units to refund
    const result = await requestServerAndReturnResponse('/refund_selected_products', {ids_and_units: ids_and_units, sale_id: sale_id}, json=true);

    // Ensure response has no errors
    if (result.errorData) {
        // Send error message
        sendPosErrorMessage(result.errorData.error, result.errorData.error);

        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    showPopOver(result.success_message, 'Refund sale');
}

// Request server to refund entire sale
async function sendSaleToRefund(event, sale_id) {
    // Prevent window reload
    event.preventDefault();

    // Request server with sale id to delete
    const result = await requestServerAndReturnResponse('/refund_sale', sale_id);

    // Ensure response has no errors
    if (result.errorData) {
        // Send error message
        sendPosErrorMessage(result.errorData.error, result.errorData.error);

        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    showPopOver(result.success_message, 'Refund sale');
}

// Send sale to validate and register
async function sendSaleToRegister(event, cash_input_value, payment_method) {
    // Prevent window reload
    event.preventDefault();

    console.log(payment_method);

    // Send request to server with cash input valus inserted
    const result = await requestServerAndReturnResponse('/register_sale', {cash_input_value:cash_input_value, payment_method: payment_method}, json=true);

    // Ensure request has no errors
    if (result.errorData) {
        // Send error message
        sendPosErrorMessage(result.errorData.error, result.errorData.error);

        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Show pop over with success message
    showPopOver(result.success_message, "Purchase concluded with success!")

    // Update sales and clients monitoring nav
    await requestActualPosSalesAndClients(event);
}

async function sendProductOrServiceToWasteOrRegularize(event, product_or_service_id, movement_type, request_for) {
    // Prevent window reload
    event.preventDefault();

    // Create a null variable
    let data;

    // Ensure which type is
    if (movement_type == 'waste') {
        // Validate waste
        await validateForm(event, document.getElementById('register_waste_form'), `/register_${request_for}_waste_or_regularization`, {product_or_service_id: product_or_service_id, movement_type: movement_type});
    }
    else {
        // Validate regularization
        await validateForm(event, document.getElementById('register_regularization_form'), `/register_${request_for}_waste_or_regularization`, {product_or_service_id: product_or_service_id, movement_type: movement_type});

    }
}


// Send service data to validate
async function sendServiceToValidateRegister(event) {
    // Prevent window reload
    event.preventDefault();

    // Get register service form element
    const form = document.getElementById('service_form');

    // Get service calculated cost price
    const service_calculated_cost_price = parseInt(document.getElementById('calculated_cost_price').innerHTML);

    const input_cost_price_value = document.getElementById('cost_price').value;

    // Ensure input_cost_price_value is higher or equal than service_calculated_cost_price
    if (service_calculated_cost_price > input_cost_price_value) {
       sendErrorMessage(event, 'Service cost price must be equal or higher than calculated service cost price.')
       throw new Error('Service cost price must be equal or higher than calculated service cost price.', '404');
    }

    // Validate form
    await validateForm(event, form, '/register_service');
      
}

async function authenticateForm(event, form_element, authenticate_type, setting_to_change) {

    // Ensure which authenticate type user selected
    if (authenticate_type == 'password') {
        route = '/authenticate_password'
    }
    else {
        route = '/authenticate_personal_code'
    }

    // Convert data from form to formData object
    const form_data = new FormData(form_element);
    
    // Add the CSRF token directly to form_data
    form_data.append('csrf_token', document.getElementById('csrf_token').value);

    // Convert form_data to a JSON object
    const form_object = Object.fromEntries(form_data.entries());

    // Request server to confirm change
    const result = await requestServerAndReturnResponse(route, form_object, json=true);

    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }
    
    console.log(result.success_message);

    if (setting_to_change == 'email') {
        await requestChangeEmailForm();
    }
    else if (setting_to_change == 'password') {
        await requestChangePasswordForm();
    }
    else if (setting_to_change == 'personal_code') {
        await requestChangePersonalCodeForm();
    }
    else if (setting_to_change == 'account') {
        showConfirmPopoverAndPersonalize(event, 'delete_account');
    }
}

// Validate POS registry
async function validatePOSregistry(event) {
    const registry_info_storaged = JSON.parse(localStorage.getItem('pos_registry'));
    console.log(registry_info_storaged);

    if (registry_info_storaged == null) {
        // Errors
        const error_message = 'Select product or service!';
        const html_error = 'Select <span class="personal-blue-color">product</span> or <span class="personal-blue-color">service</span>!</h5>'
                
        // Send Pos error message
        sendPosErrorMessage(error_message, html_error);

    }

    if (registry_info.innerHTML != '') {
        if (registry_info.innerHTML.indexOf('x') == -1) {
            // Errors
            const error_message = 'Insert X to multiply product or service!';
            const html_error = 'Insert <span class="personal-blue-color">X</span> to <span class="personal-blue-color">multiply</span>!</h5>';
                    
            // Send Pos error message
            sendPosErrorMessage(error_message, html_error);
                
        }

        // Get units inserted by user
        const units_multiply_sign = registry_info.innerHTML.split(" ");
        console.log(units_multiply_sign);

        // Insert key,value in to registry_info_storaged
        registry_info_storaged[0]["units"] = Number(units_multiply_sign[0]);
    }
    else {
        registry_info_storaged[0]["units"] = 1;
    }

    console.log(registry_info_storaged);

    // Register purchase
    await registerRegistry(event, registry_info_storaged);
}

async function validateForm(event, form_element, route, extra_arg=undefined, form_reset=true) {
 
    // Convert data from form to formData object
    const form_data = new FormData(form_element);

    if (extra_arg != undefined) {
        if (typeof(extra_arg) == 'string') {
            form_data.append('id', extra_arg);
        }
        else {
            form_data.append('extra_form_data', JSON.stringify(extra_arg))
        }
    }
    
    // Add the CSRF token directly to form_data
    form_data.append('csrf_token', document.getElementById('csrf_token').value);

    // Convert form_data to a JSON object
    const form_object = Object.fromEntries(form_data.entries());

    console.log(form_object);

    // Sanitize form data
    form_data.forEach(data => {
        sanitizeInput(data);
    })

    console.log(form_object);

    // Request server to confirm change
    const result = await requestServerAndReturnResponse(route, form_object, json=true);

    if (result.errorData) {

        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    showPopOver(result.success_response, "Success!");

    if (form_reset) {
        // Reset form
        form_element.reset();
    }
}

// Set session store status to open
async function openStore(event) {
    // Prevent window reload
    event.preventDefault();

    // Send request to change session store status open
    const response = await fetch('/open_store', {method: "POST"});

    const result = await response.json();

    // Ensure response has no errors
    if (result.errorData) {
        // Send error message to user
        sendPosErrorMessage(result.errorData.error, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    await requestIndexMainInfo();

}

// Set session store status to closed
async function closeStore(event) {
    // Prevent window reload
    event.preventDefault();

    // Send request to change session store status open
    const response = await fetch('/close_store', {method: "POST"});

    const result = await response.json();

    // Ensure response has no errors
    if (result.errorData) {
        // Send error message to user
        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    await requestIndexMainInfo();

    showPopOver(result.sales_report_html, "Sales report")

}

// Request server to start monitoring sales and clients
async function startMonitoringSalesAndClients(event) {
    // Prevent window reload
    event.preventDefault();

    // Send request to change session store status open
    const response = await fetch('/start_monitoring', {method: "POST"});

    const result = await response.json();

    // Ensure response has no errors
    if (result.errorData) {
        // Send error message to user
        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    // Request index main info
    requestIndexMainInfo();

}

// Request server to stop monitoring sales and clients
async function stopMonitoringSalesAndClients(event) {
    // Prevent window reload
    event.preventDefault();

    // Send request to change session store status open
    const response = await fetch('/stop_monitoring', {method: "POST"});

    const result = await response.json();

    // Ensure response has no errors
    if (result.errorData) {
        // Send error message to user
        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    requestIndexMainInfo();

}

// Start POS system
async function startPOS(event) {
    // Prevent window reload
    event.preventDefault();

    // Send request to change session store status open
    const response = await fetch('/start_pos', {method: "POST"});

    const result = await response.json();

    // Ensure response has no errors
    if (result.errorData) {
        // Send error message to user
        sendErrorMessage(event, result.errorData.error);
        throw new Error(`Error ${result.status}: ${result.errorData.error}`);
    }

    document.getElementById('index_body').innerHTML = result.start_pos_html;

    // Manual bar code reader select button
    const manual_bar_code = document.getElementById('bar_code_manual');
    
    // Add event listener to manual bar code select button
    manual_bar_code.addEventListener('click', async function(event) {
        // Request POS content
        await requestPOS(event, "manual_mode");
    })

    // Scan bar code reader select button
    const scan_bar_code_reader = document.getElementById('scan_bar_code_reader');

    // Add event listener to scan bar code reader select button
    scan_bar_code_reader.addEventListener('click', async function (event) {
        // Request POS content
        await requestPOS(event, "scan_mode");        
    })
}

// Validate and register purchase registry
async function registerRegistry(event, registry_info_storaged) {
    // Prevent window reload
    event.preventDefault();

    // Send request with registry info storaged
    const result = await requestServerAndReturnResponse('/register_registry', registry_info_storaged, json=true);

    if (result.errorData) {
        // Send Pos error message
        sendPosErrorMessage(result.errorData.error, result.errorData.error);
    }

    // Request POS purchase info
    await requestPosPurchaseInfo(event);

    // Clean registry info html
    registry_info.innerHTML = '';

    // Clean product or service input value
    document.getElementById('insert_product_or_service').value = '';

    // Clean bar code h5 element
    document.getElementById('bar_code').innerHTML = '';

    // Clean localStorage
    localStorage.removeItem('pos_registry');

}

// Delete last POS registry
async function deletePosRegistry(event, index) {
    // Prevent window reload
    event.preventDefault();

    // Request server to delete last pos registry and get updated pos_purchase_info.html
    await requestServerAndReturnResponse('/delete_pos_registry', index);
}

// Logout user and redirect to login route in 3 seconds
function logoutUserAndRedirectToLogin() {
    setInterval(async function () {
        // Logout user
        await logoutUser();

        // Redirect user to login
        window.location.href = '/login';
    }, 3000)
}

// Request server to logout user
async function logoutUser() {
   await fetch("/logout");
}

// Delete last POS registry
async function copyPosLastRegistry(event, index) {
    // Prevent window reload
    event.preventDefault();

    // Request server to delete last pos registry and get updated pos_purchase_info.html
    await fetch('/copy_pos_last_registry');
}

// ----------------------------------------- UTILITIES ------------------------------------------------------------\\

// Add Sucess Message 
function sendSucessMessage(event, message, popover=false) {

    // Closest element
    if (popover) {
        closest_element = document.getElementById('popover-message')
    }
    else {
        
        closest_element = event.target.closest('.user-form');
    }

    // Message element from button clicked closest element 
    const message_element = closest_element.querySelector('.message');

    // Add error border to abled input
    document.querySelectorAll('input').forEach(input => {
        if (!input.disabled) {
            input.classList.remove('error-border');
        }
    })

    // Add sucess-message class
    message_element.classList.add('sucess-message');

    // Remove error-message class
    message_element.classList.remove('error-message');

    // Insert message in message element html
    message_element.innerHTML = message;

    // Clean message after 5sec
    setTimeout(function() {
        message_element.innerHTML = '';
    }, 10000);

}

// Add Error Message 
function sendErrorMessage(event, message, popover=false) {
   
    // Closest element
    if (popover) {
        closest_element = document.getElementById('popover-message')
    }
    else {
        
        closest_element = event.target.closest('.user-form');
    }

    console.log(closest_element);

    const message_element = closest_element.querySelector('.message');

    // Add sucess-message class
    message_element.classList.add('error-message');

    // Add error border to abled input
    closest_element.querySelectorAll('input, select').forEach(input => {
        if (!input.disabled && input.type != 'radio' && input.type != 'search') {
            input.classList.add('error-border');
        }
    })

    // Remove sucess-message class
    message_element.classList.remove('sucess-message'); 

    // Insert message in message element html
    message_element.innerHTML = message;

    // Clean message and borders after 5seconds
    setTimeout(function() {
        message_element.innerHTML = '';
        document.querySelectorAll('input, select').forEach(input => {
            if (!input.disabled && input.type != 'radio' && input.type != 'search') {
                input.classList.remove('error-border');
            }
        })

    }, 6000);

}

// Send POS error messages
function sendPosErrorMessage(error, html_error) {

    document.querySelector('.personal-pop-over').classList.add('show-pop-over');

    document.querySelector('.pop-over-content-body').innerHTML = html_error;
                    
    document.getElementById('edit_title').innerHTML = 'Tip error';

    throw new Error(error);
}


// Allow Bootstrapp tootips
function allowToolTips() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})
}

// Get my_products_and_services search filters
function getMyProductsAndServiceSearchFilters() {
    // Description or bar code filter
    let description_bar_code_filter = document.getElementById('description_bar_code_filter').value;
    
    // Sanitize description_bar_code_filter
    description_bar_code_filter = sanitizeInput(description_bar_code_filter)

 
    // Type filter
    let type_filter = document.getElementById('type_filter').value;
    
    // Ensure user want to search for product, service or all and handle category and sub categories
    let category_filter;
    let sub_category_filters = [];

    if (type_filter == 'product') {
        // Category filter value
        category_filter = document.getElementById('category_filter').value;

        // Ensure category filter value is not 'All' else convert to default value
        if (category_filter == 'All') {
            category_filter = '';
        }
        else {
            // Sub categories check options
            const sub_categories_options = document.getElementsByName('sub_category_filter');
        
            // Get checked sub categories to search
            sub_categories_options.forEach(option => {
                if (option.checked) {

                    // Append sub category id to sub_category_filters array
                    sub_category_filters.push(sanitizeInput(option.value));
                }
            })

           
        }
    } 
    else if (type_filter == 'service') {
            // Default values
            category_filter = '';
    }
    else {
        // Default values
        type_filter = '';
        category_filter = '';
    }

    // Order by filter
    const order_by_filter = document.getElementById('order_by_filter').value;

    // Order by asc or desc filters
    const order_by_asc_desc_options = document.getElementsByName('asc_desc_filter');

    let order_by_asc_desc_filter;
    
    // Itherate order_by_asc_desc_options and get checked one
    order_by_asc_desc_options.forEach(option => {
        if (option.checked) {
            order_by_asc_desc_filter = option.value;
        }
    })


    // Filters
    const filters = {
        description_bar_code_filter: sanitizeInput(description_bar_code_filter),
        type_filter: sanitizeInput(type_filter),
        category_filter: sanitizeInput(category_filter),
        sub_category_filters: sub_category_filters,
        order_by_filter: sanitizeInput(order_by_filter),
        order_by_asc_desc_filter: sanitizeInput(order_by_asc_desc_filter)
    };

    console.log(filters);

    // Return filters
    return filters;
}

// Get service info and return an array
function getServiceInfo() {
    // Empty array
    service_info = [];

    // Get service description
    let description = document.getElementById('service_description').value;
    
    // Service cost price
    const cost_price = document.getElementById('cost_price').value;

    // Service sell price
    const sell_price = document.getElementById('sell_price').value;

    // Append service description, cost price and sell price in service info array
    service_info.push({description: sanitizeInput(description)});
    service_info.push({cost_price: sanitizeInput(cost_price)})
    service_info.push({sell_price: sanitizeInput(sell_price)})

    // Empty array for product associated and stock to deduct
    products_and_stocks = [];

    // Service product inputs
    const service_product_inputs = document.getElementsByName('service_product');

    // Service product stock
    const service_stock_inputs = document.getElementsByName('service_stock');


    // Loop throgh service product and stock inputs and append info to service products array
    for (let i = 0; i < service_product_inputs.length; i++) {
        const product = service_product_inputs[i].value;
        const stock = service_stock_inputs[i].value;
        products_and_stocks.push({product:product, stock:stock});
    }

    // Append service products and stocks associated to service info array
    service_info.push({products_and_stocks: products_and_stocks});

    console.log(service_info);

    // Return array with service info
    return service_info
}

// Adjust elements size when window resize
function adjustElements() {

    // get nav side element
    const nav_side_box = document.getElementById('nav-side-box');

    if (nav_side_box) {
        // Get windows width
        let width = window.innerWidth;

        // off canvas nav side button
        const off_canvas = `
        <button class="btn dropdown-toggle" id="off_canvas_button" type="button" data-bs-toggle="offcanvas" data-bs-target="#nav-side-box">Apps</button>`;
        
        // get element to put append off canvas button
        const off_canvas_button_element = document.getElementById('off_canvas_button');

        // if window width less than 576 pixels
        if (width < 576) {
                // ensure if nav side off canvas button already doesnt exists
                if (off_canvas_button_element == null) {

                    // add off-canvas bootstrapp class to nav-side button
                    nav_side_box.setAttribute('class', 'offcanvas offcanvas-start')
                    document.getElementById('nav-side').setAttribute('class', 'offcanvas-body');
                    
                    // add canvas head and close button
                    const canvas_head_button = `<div class="offcanvas-header" id="canvas_header">
                                                    <h1 class="offcanvas-title personal-blue-color f-bold">Apps</h1>
                                                <button type="button" class="btn-close" data-bs-dismiss="offcanvas"></button></div>`

                    nav_side_box.insertAdjacentHTML('afterbegin', canvas_head_button);

                    // add off-canvas button nav-bar
                    document.getElementById('off_canvas_button_box').innerHTML = off_canvas;

                    // Get header classes
                    const header_class = document.querySelector('header').getAttribute('class');
                    // Update header classes
                    document.querySelector('header').setAttribute('class', header_class + ' shadow bg-white');

            }    
        } 
        else {
            // ensure if nav side off canvas buttom already exists
            if (off_canvas_button_element != null) {

                // remove off canvas classes
                nav_side_box.setAttribute('class','');
                document.getElementById('nav-side').setAttribute('class', 'border-end border-top');

                // remove off canvas button
                document.getElementById('off_canvas_button').remove();

                // remove canvas header
                document.getElementById('canvas_header').remove();

                document.getElementById('off_canvas_button_box').innerHTML = '';

            }            
        }
    }
}

// Simulate click event
function simulateClickEvent(button) {

    // Simulate event click in home button
    const clickEvent = new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: true
    });

    button.dispatchEvent(clickEvent);

}

// Function to sanitize input
function sanitizeInput(input) {
    var element = document.createElement('div');
    element.appendChild(document.createTextNode(input));
    return element.innerHTML;
}

// Add event listener to close por over button
function closePopOverButton() {
    // Get close pop-over button
    const close_pop_over_button = document.querySelectorAll('#close-pop-over');

    if (close_pop_over_button) {
        close_pop_over_button.forEach(button => {
            button.addEventListener('click', function(event) {

                // Get closest pop-over element
                const pop_over = event.target.closest('.personal-pop-over');
        
                // Remove show-pop-over class from pop-over
                pop_over.classList.remove('show-pop-over');
        
                // Remove 'editing' class from table row that was beeing edited
                document.querySelectorAll('tr').forEach(row => {
                    if (row.classList.contains('editing')) {
                        row.classList.remove('editing');
                    }
                })
                
                // Ensure popover has a form
                const popover_form = pop_over.querySelector('form');

                // Reset form
                if (popover_form) {
                    pop_over.querySelector('form').reset();
                }
                
                // Clean error messages and error borders
                document.querySelectorAll('input, select').forEach(input => {
                    input.classList.remove('error-border');
                })

                sendSucessMessage(event, '');

                // New inventory storage data
                const new_inventory_storaged_data = JSON.parse(sessionStorage.getItem('new_inventory'));

                // Ensure session is not empty
                if (new_inventory_storaged_data != null) {
                    sessionStorage.clear('new_inventory');
                }
                
            })
        })

    }
}

// Handle tables pagination
function handlePaginationButtonsAndUpdateResults(event, table, data=null, extra_arg=null) {
   
    // Active page index
    let active_page_index = document.querySelector('.page-item > .active').innerHTML;

    // Convert to integer active page index
    active_page_index = parseInt(active_page_index);

    active_page_index = active_page_index - 1

    let pagination_index;

    if (event.target.id == 'previous_page') {
        pagination_index = active_page_index - 1;
    }
    else {
        pagination_index = active_page_index + 1;
    }

    if (table == 'my_products_search') {
        requestMyProductsAndServiceSearchFilters(event, pagination_index);
    }

    if (table == 'order_table') {
        requestOrderTableAndUpdate(pagination_index);
    }

    if (table == 'movements_table') {
        requestProductOrServiceMovements(event, data, pagination_index, extra_arg);
    }

    if (table == 'inventory_table') {
        requestCategoriesProductsToSelectToInventory(event, pagination_index);
    }

    if (table == 'inventory_info') {
        requestInventoryInfo(event, data, pagination_index);
    }

    if (table == 'count_inventory') {
        requestCountInventoryForm(event, data, pagination_index);
    }

    if (table == 'finish_inventory') {
        requestFinishInventoryForm(event, data, pagination_index);
    }

    if (table == 'closed_inventory') {
        requestClosedInventoryInfo(event, data, pagination_index);
    }

    if (table == 'without_sales_info') {
        requestProductsWithoutSalesInfo(event, pagination_index);
    }

    if (table == "negative_stock" || table == "null_stock") {
        requestProductsIndexStockInfo(event, pagination_index, table);
    }

    if (table == 'sale_info') {
        requestRefundSaleMenu(event, pagination_index);
    }

    console.log(table);
}

// Handle service register products associated form 
function AddOrRemoveProductFromServiceInputHandler () {
    // Button that add select and input products to service
    const add_select_input_button = document.getElementById('add_select_input');

    // Button that remove select and input products to service
    const remove_select_input_button = document.getElementById('remove_select_input');

    add_select_input_button.addEventListener('click', function(event) {
        // Prevent window reload
        event.preventDefault();
        
        // Get form
        const service_form = document.getElementById('service-form-content');

        // Get select element thats is active
        const active_select_input = document.querySelector('.active_select_input');

        // Get selected product and stock to deduct elements
        const active_select = active_select_input.querySelector('select');
        const active_input = active_select_input.querySelector('input');

        // Get stock input id 
        let stock_input_id = active_input.id;
        let product_select_id = active_select.id;
        
        // Ensure user fullfill stock input
        if (active_input.value == "") {
            sendErrorMessage(event, "Please complete product stock field!");   
            return;
        }

        if (active_input.value <= 0) {
            sendErrorMessage(event, "Stock must be a positive value!");
            return;
        }

        // Clone element 
        const new_active_select_input = active_select_input.cloneNode(true);

        console.log(new_active_select_input);

        // Get cloned element input and select elements
        const new_active_input = new_active_select_input.querySelector('.form-control');
        const new_active_select = new_active_select_input.querySelector('select');
        const new_active_token = new_active_select_input.querySelector('input');

        // Clean new_active_select_input
        new_active_input.value = "";

        const all_service_products_content_elements = document.querySelectorAll('.select-service-products-content');

        // Change new element label 'for' attribute and input 'id' of service stock
        new_active_input.id = `products_associated-${all_service_products_content_elements.length.toString()}-stock_associated`;
        new_active_input.name = `products_associated-${all_service_products_content_elements.length.toString()}-stock_associated`;
        new_active_select_input.querySelector('.service_stock_label').setAttribute('for', `products_associated-${all_service_products_content_elements.length.toString()}-stock_associated`);

        // Change new element label 'for' attribute and input 'id' of service product
        new_active_select.id = `products_associated-${all_service_products_content_elements.length.toString()}-product`;
        new_active_select.name = `products_associated-${all_service_products_content_elements.length.toString()}-product`;
        new_active_select_input.querySelector('.service_product_label').setAttribute('for', `products_associated-${all_service_products_content_elements.length.toString()}-product`);

        new_active_token.id = `products_associated-${all_service_products_content_elements.length.toString()}-csrf_token`;
        new_active_token.name = `products_associated-${all_service_products_content_elements.length.toString()}-csrf_token`;

        // Remove active_select class from first active_select
        active_select_input.classList.remove('active_select_input');

        // Get list of optioms of new_active_select
        const list_of_options = new_active_select_input.querySelectorAll('option');
 
        // Loop through options of new active select element and remove which one is selected in older select element
        list_of_options.forEach(option => {
            if (option.value === active_select.value) {
                option.remove();
            }
        })


        // Disable button if only one option available
        if (list_of_options.length == 2) {
            add_select_input_button.disabled = true;
        }

        // Insert new select element in form
        service_form.appendChild(new_active_select_input);

        document.querySelectorAll('.stock').forEach(input => {
            input.addEventListener('input', requestServiceCalculatedCostPrice);
        })
      
        // Able remove input button
        remove_select_input_button.disabled = false;
    })

    remove_select_input_button.addEventListener('click', function(event) {
        // Prevent window reload        
        event.preventDefault();

        // Get all service products inputs
        let all_service_products_inputs = document.querySelectorAll('.select-service-products-content');

        // Remove last service product input
        all_service_products_inputs[all_service_products_inputs.length-1].remove();

        // Add active_select class to new last service product input
        all_service_products_inputs[all_service_products_inputs.length-2].classList.add('active_select_input');

        // Get select element thats is active
        const active_select = document.querySelector('.active_select_input');

        active_select.querySelector('select').disabled = false;
        active_select.querySelector('input').disabled = false;

        // If only one service product input
        if (all_service_products_inputs.length == 2) {
            remove_select_input_button.disabled = true;
        }

        // Able add input button
        add_select_input_button.disabled = false;

    })
}

// Show confirm popover and personalize
async function showConfirmPopoverAndPersonalize(event, button_value, arg=undefined) {
    // Prevent window reload
    event.preventDefault();

    // Get popover element and add show-pop-over class
    var popover = document.querySelector('.confirm-pop-over');

    // Add show-pop-over class to confirm pop over
    popover.classList.add('show-pop-over');

    // Get confirm_submit button
    var confirm_submit_button = document.getElementById('confirm_submit');

    // Get cancel_submit button
    var cancel_submit_button = document.getElementById('cancel_submit');

    // Add event listener to cancel submit button
    cancel_submit_button.addEventListener('click', function() {
        // Close pop over
        popover.classList.remove('show-pop-over');
    })

    // Get popover-question element
    const popover_question = document.querySelector('.popover-question');

    async function handleConfirmRequest(request_function, arg=undefined) {

        // Add event listener to confirm_submit_button
        confirm_submit_button.addEventListener('click', async function(event) {

            if (!arg) {
                await request_function(event);
            }
            else {
                // Request server to remove all products from register list
                await request_function(event, arg);
            }

            // Close pop over
            popover.classList.remove('show-pop-over');

        }, {once: true});   
    }

    console.log(button_value);
    
    // Ensure which button value is passed
    if (button_value == 'confirm_remove_all_products_from_register_list') {
       
        // Change message to user in popover-question element
        popover_question.innerHTML = 'Are you sure you want to remove all products?';

        await handleConfirmRequest(removeAllProductsFromRegisterList);

    }
    else if (button_value == 'confirm_register_products') {
        // Change message to user in popover-question element
        popover_question.innerHTML = 'Are you sure you want to register the products?';

        await handleConfirmRequest(registerProducts);
    }

    else if (button_value == 'delete_product') {
        // Change message to user in popover-question element
        popover_question.innerHTML = 'Are you sure you want to delete the product?'

        await handleConfirmRequest(sendProductToDelete, arg=arg);

    }
    else if (button_value == 'delete_service') {
        // Change message to user in popover-question element
        popover_question.innerHTML = 'Are you sure you want to delete the service?'

        await handleConfirmRequest(sendServiceToDelete, arg=arg);
        
    }
    else if (button_value == 'delete_inventory' ){
        // Change message to user in popover-question element
        popover_question.innerHTML = 'Are you sure you want to delete inventory?'

        // Inventory id empty value
        let inventory_id = confirm_submit_button.value;

        await handleConfirmRequest(sendProductToDelete, arg=inventory_id);

    }
    else if (button_value == 'close_day') {
        // Change message to user in popover-question element
        popover_question.innerHTML = 'Are you sure you want to close store? Sales and clients monitoring will stop and a day report will be showed!'

        await handleConfirmRequest(closeStore);

    }
    else if (button_value == 'delete_account') {
        // Change message to user in popover-question element
        popover_question.innerHTML = 'Are you sure you want to delete your account?!'

        // Create <a> element
        const link_element = document.createElement('a');
        link_element.innerHTML= confirm_submit_button.innerHTML;
        link_element.class += confirm_submit_button.class
        link_element.href = '/delete_account';
        confirm_submit_button.replaceWith(link_element);
    }
}

// Add to personal-pop-over element class 'show-pop-over' and insert content
function showPopOver(content, title) {
    // Add 'show-pop-over' class
    document.querySelector('.personal-pop-over').classList.add('show-pop-over');

    // Insert content in pop over body
    document.querySelector('.pop-over-content-body').innerHTML = content;

    // Change pop over title
    document.getElementById('edit_title').innerHTML = title;
}

// Handle product system side nav bar buttons
function changeActiveMainButton (event) {

    const active_row = document.querySelector('.active');

    const closest_button = event.target.closest('a');

    const active_sub_row = document.querySelector('.sub_active');


    console.log(closest_button.name);

    if (closest_button.name != 'add_product') {
               
        if (active_sub_row) {
            active_sub_row.classList.remove('sub_active');
        }
    }

    
    if (active_row) {
        active_row.classList.remove('active');

    }

    // Add active class to link clicked
    closest_button.classList.add('active')
}

// Request server and return response
async function requestServerAndReturnResponse(route, data_to_send, json=false, csrf_token=false) {
    
    // Request info to send to browser
    let request;

    // Ensure data to send is in json format 
    if (json) {
        
        request = {
            method: "POST",
            headers: {'Content-type': 'application/json'},
            body: JSON.stringify(data_to_send)
        };
    }
    else if (json && csrf_token) {
        request = {
            method: "POST",
            headers: {'Content-type': 'application/json', 'X-CSRFToken': csrf_token},
            body: JSON.stringify(data_to_send)
        };
    }
    else {

        request = {method: "POST", body: data_to_send};
    }

    try {
        // Send request with worker id
        const response = await fetch(route, request);

        if (!response.ok) {

            const errorData = await response.json();

            return {errorData: errorData,
                status: response.status
        };
        }

        // Request response result
        const result = await response.json();

        console.log(result.sucess_message);

        // Return response result
        return result;

    }
    catch (error) {
        console.log(error);
    }    
}

// Use sessionStorage so storage inventory counts helping in dinamic pagination
function storageInventoryCounts(inventory_id) {
    // Add event listener to all count inputs
    document.getElementsByName('count_input').forEach(input => {
        input.addEventListener('input', function (event) {

            // Product id and stock value
            const product_id = event.target.closest('tr').id;
            const stock_value =  event.target.value
            
            // Product count data to storage
            inventory_product = {product_id: sanitizeInput(product_id), stock_value: sanitizeInput(stock_value)};


            // Ensure storage is null
            if (sessionStorage.getItem(inventory_id) == null) {
                // Create storage
                sessionStorage.setItem(inventory_id, JSON.stringify([inventory_product]));

                console.log("first")
            }
            // Already created store
            else {
                // Get data already stored
                const storaged = JSON.parse(sessionStorage.getItem(inventory_id));

                // Ensure product is already storaged
                let already_storaged = false;
                for (let i = 0; i < storaged.length; i++) {
                    if (storaged[i].product_id == product_id) {
                        // Update product count
                        storaged[i].stock_value = stock_value; 
                        // Set already_storage to true
                        already_storaged = true;
                    }
                }

                // If not storage, update array
                if (!already_storaged) { 
                    storaged.push(inventory_product);
                }

                // Create updated storage data
                sessionStorage.setItem(inventory_id, JSON.stringify(storaged));
            }

            console.log(sessionStorage.getItem(inventory_id));
        })
    })
}

function handlePersonalCodeInput() {
    // Personal code inputs
    const personal_code_inputs = document.querySelectorAll('.personal_code');

    // Itherate personal code inputs
    personal_code_inputs.forEach(input => {
        input.addEventListener('input', function(event) {
            // Allowed digits
            const allowed_digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

            // Last digit inserted
            const last_digit_inserted = event.target.value.slice(-1);

            // Ensure user input numbers
            if (!allowed_digits.includes(last_digit_inserted) && input.value != '') {
                event.target.value = event.target.value.slice(0, -1);
            }
        })
    })
}

// Use sessionStorage so storage inventory counts helping in dinamic pagination
function storageInventoryProductsToRecount(inventory_id) {
    // Add event listener to all send to recount check inputs
    document.getElementsByName('send_to_recount').forEach(check => {
        check.addEventListener('input', function (event) {

            // Product id and stock value
            const product_id = event.target.id;

            if (check.checked) {
            
                // Products array to storage products id
                inventory_products = [];

                // Ensure storage is null
                if (sessionStorage.getItem(inventory_id) == null) {
                    // Append to array
                    inventory_products.push(sanitizeInput(product_id));

                    // Create storage
                    sessionStorage.setItem(inventory_id, JSON.stringify(inventory_products));
                }
                // Already created storage
                else {
                    // Get data already stored
                    const storaged = JSON.parse(sessionStorage.getItem(inventory_id));

                    // Append new product id to already storaged data
                    storaged.push(product_id);

                    // Create updated storage data
                    sessionStorage.setItem(inventory_id, JSON.stringify(storaged));
                }
            }
            else {
                // Get data already stored
                const storaged = JSON.parse(sessionStorage.getItem(inventory_id));

                // Remove product id from already storaged data
                let updated_storaged = storaged.filter(item => item !== product_id);

                console.log("remove");

                // Create updated storage data
                sessionStorage.setItem(inventory_id, JSON.stringify(updated_storaged));
            }

            console.log(sessionStorage.getItem(inventory_id));
        })
    })
}

// Clean sessionStorage
function cleanSessionStorage(item) {

    sessionStorage.removeItem(item);
}

// Use sessionStorage so storage inventory counts helping in dinamic pagination
function storageProductsToCreateInvetory() {
    // Add event listener to all send product to inventory inputs
    document.getElementsByName('send_to_inventory').forEach(check => {
        check.addEventListener('input', function (event) {

            // Product id and stock value 
            const product_id = event.target.id;

            if (check.checked) {
                if (sessionStorage.getItem('new_inventory')  == null) {
                    sessionStorage.setItem('new_inventory', JSON.stringify([product_id]));
                }
                else {
                    // Storaged data
                    const storaged = JSON.parse(sessionStorage.getItem('new_inventory'));

                    console.log(storaged);

                    // Append to storaged
                    storaged.push(product_id);

                    // Update sessionStorage object
                    sessionStorage.setItem('new_inventory', JSON.stringify(storaged));
                }
            }
            else {
                // Storaged data
                const storaged = JSON.parse(sessionStorage.getItem('new_inventory'));

                // Remove from storaged
                storaged.pop(product_id);

                // Update sessionStorage object
                sessionStorage.setItem('new_inventory', JSON.stringify(storaged));
            }

            console.log(JSON.parse(sessionStorage.getItem('new_inventory')));
        })

    })
}


