from datetime import datetime

class DataBaseHelper:
    """ Class with database functions iniated with user id and db conncection """

    def __init__(self, db_connection, user_id=None, email=None):
        self.db = db_connection

        if email is not None:
            user_result = self.db.execute("SELECT id FROM users WHERE email = ?", email)

            if user_result:
                self.user_id = user_result[0]["id"]
            else:
                self.user_id = None

        else:
            self.user_id = user_id

        if self.user_id is not None:

            company_result = self.db.execute("SELECT id from companies WHERE user_id = ?", (self.user_id))

            if company_result:
                self.company_id = company_result[0]["id"]
                self.user = self.db.execute("SELECT * FROM users WHERE id = ?", (self.user_id))
            else:
                self.company_id = None
                self.user = None

        else:
            self.company_id = None
            self.user = None

    def get_user(self):
        """ Return user information """

        return self.user

    def query_user_personal_code(self):
        """ Query user personal code """

        # Query user personal code
        personal_code = self.db.execute("SELECT personal_code FROM users WHERE id = ?", self.user_id)

        return personal_code

    def begin_transaction(self):
        """ Begin SQL transaction """
        self.db.execute("BEGIN TRANSACTION")

    def commit(self):
        """ Commit SQL transaction """
        self.db.execute("COMMIT")

    def rollback(self):
        """ Rollback SQL transaction """
        self.db.execute("ROLLBACK")

    def query_company(self):
        """ Query user company info """

        company_info = self.db.execute("SELECT * FROM companies where id = ?", self.company_id)

        return company_info
    
    def query_company_id(self):
        """ Return company id """

        return self.company_id

    def query_all_products(self):
        """ Query all company products from products table """
        
        # Query all products from database
        products = self.db.execute("""SELECT products.id, products_basic.description, products_basic.bar_code, products_basic.category, products_basic.sub_category,
                                   products_financial.stock, products_financial.cost_price, products_financial.sell_price, products_financial.margin_percentage, products_financial.unity_m
                                   FROM products
                                   INNER JOIN products_basic
                                   ON products.id = products_basic.product_id
                                   INNER JOIN products_financial
                                   ON products.id = products_financial.product_id
                                   AND products.id IN (SELECT id FROM products WHERE company_id = ?)""", self.company_id)
        
        # Return all products
        return products
    
    def query_product(self, product_id: str) -> list:
        """ Query product information """

        # Query product information
        product = self.db.execute("""SELECT products.id, products_basic.description, products_basic.bar_code, products_basic.category, products_basic.sub_category, products_financial.stock, products_financial.cost_price, products_financial.sell_price, products_financial.margin_percentage, products_financial.unity_m
                                  FROM products
                                  INNER JOIN products_basic ON products.id = products_basic.product_id 
                                  INNER JOIN products_financial ON products.id = products_financial.product_id 
                                  WHERE products.id = ?""", product_id)
        
        return product
    
    def query_products_ids(self, limit=1) -> list:
        """ Query company products ids from products table """

        products_ids = self.db.execute(f"SELECT id FROM products WHERE company_id = ? ORDER BY id DESC LIMIT {limit}", self.company_id)

        return products_ids
    
    def query_product_id(self, description: str) -> list:
        """ Query product id from products table """

        # Query product id
        product_id = self.db.execute("SELECT id from products WHERE id = (SELECT product_id FROM products_basic WHERE description = ? AND products.company_id = ?)", description, self.company_id)

        # Return product_id
        return product_id
    
    def query_products_basic(self):
        """ Query all products basic information from products_basic table """

        products_basic = self.db.execute("SELECT * FROM products_basic WHERE product_id IN (SELECT id FROM products WHERE company_id = ?) ORDER by description ASC", self.company_id)

        # Return products basic
        return products_basic
    
    def query_product_financial(self, product_id: str) -> list:
        """ Query for product financial information """

        # Query product prices
        product_financial = self.db.execute("SELECT * FROM products_financial WHERE product_id = ?", product_id)

        # Return product prices list
        return product_financial
    
    def query_service(self, service_id: str) -> str:
        """ Query service info """

        # Query service info
        service = self.db.execute("""SELECT services_basic.description, services_basic.bar_code, services_financial.cost_price, services_financial.sell_price, services_financial.margin_percentage
                                  FROM services_basic
                                  INNER JOIN services_financial
                                  ON services_basic.service_id = services_financial.service_id
                                  WHERE services_basic.service_id = ?""", service_id)
        # Return service info
        return service
    
    def query_services(self):
        """ Query company services """

        # Query services
        services = self.db.execute("SELECT * FROM services WHERE company_id = ?", self.company_id)

        # Return services
        return services

    def query_services_basic(self) -> list:
        """ Query services basic information from services_basic table """

        # Query all product services from database
        services = self.db.execute("SELECT * FROM services_basic WHERE service_id IN (SELECT id FROM services where company_id = ?)", self.company_id)

        # Return all user services
        return services
    
    def query_service_products(self, service_id: str) -> list:
        """ Query service products from service_products table """

        # Query service products
        service_products = self.db.execute("SELECT * FROM services_products WHERE service_id = ?", service_id)

        # Return service products
        return service_products

    def query_edit_search_results(self, search_value: str) -> list:
        """ Query products and services tables and return results """

        # Create empty list to save search results
        search_results = []

        # Query products tables with search value
        products = self.db.execute("""SELECT "Product" AS type, products.id, products_basic.description, products_basic.bar_code, products_basic.category, products_basic.sub_category, products_financial.cost_price, products_financial.sell_price, products_financial.margin_percentage, products_financial.unity_m
                                      FROM products_basic 
                                      INNER JOIN products_financial
                                      ON products_basic.product_id = products_financial.product_id
                                      INNER JOIN products
                                      ON products_financial.product_id = products.id
                                      WHERE products_basic.description LIKE ? OR products_basic.bar_code LIKE ? AND products.company_id = ?
                                      LIMIT 10
                                      """, "%" + search_value + "%", "%" + search_value + "%", self.company_id)
        
        # Query services table with search value
        services = self.db.execute(""" SELECT "Service" AS type, "--" as category, "--" as sub_category, services.id, services_basic.description, services_basic.bar_code, services_financial.cost_price, services_financial.sell_price, services_financial.margin_percentage, services_financial.unity_m
                                       FROM services
                                       INNER JOIN services_financial
                                       ON services.id = services_financial.service_id
                                       INNER JOIN services_basic
                                       ON services_financial.service_id = services_basic.service_id
                                       WHERE services_basic.description LIKE ? AND services.company_id = ?
                                       LIMIT 10""", "%" + search_value + "%", self.company_id)

        # Concatenate two results
        search_results = products + services

        # Return results
        return search_results
    
    def query_search_my_products_with_filters(self, filters: dict, pagination_index=None, limit=None, sub_categories_filter=None) -> list:
        """ Search products with based in filters """

        print(filters)

        # Search filters
        description_bar_code_filter = filters["description_bar_code_filter"]
        category_filter = filters["category_filter"]
        order_by_filter = filters["order_by_filter"]
        asc_desc_filter = filters["asc_desc_filter"]

         # Search parameters
        params = ["%" + description_bar_code_filter + "%", "%" + description_bar_code_filter + "%", "%" +  category_filter + "%", self.company_id]

        # Default query
        default_query = """SELECT "Product" AS type, products.id, products_basic.description, products_basic.bar_code, products_basic.category, products_basic.sub_category, products_financial.cost_price, products_financial.sell_price, products_financial.margin_percentage, products_financial.unity_m, products_financial.stock
                                      FROM products_basic 
                                      INNER JOIN products_financial
                                      ON products_basic.product_id = products_financial.product_id
                                      INNER JOIN products
                                      ON products_financial.product_id = products.id
                                      WHERE (products_basic.description LIKE ? OR products_basic.bar_code LIKE ?)
                                      AND products_basic.category LIKE ?
                                      AND products.company_id = ?
                                      """
        
        # Ensure sub_category_filters is not empty
        if sub_categories_filter is not None:
            # Create placeholders
            placeholders = " ,".join("?" for _ in sub_categories_filter)

            # Sub category filter query
            sub_category_filters_query = f" AND products_basic.sub_category IN ({placeholders})"

            
            # Concatenate default query plus sub category filters
            default_query += sub_category_filters_query

            # Extend search parameters list
            params.extend(sub_categories_filter) 

        else:
            # Sub category filter query
            sub_category_filters_query = " AND products_basic.sub_category LIKE '%%'"

            # Concatenate default query plus sub category filters
            default_query += sub_category_filters_query

      
        # Order query
        order_query = f"ORDER BY {order_by_filter} {asc_desc_filter}"

        if pagination_index is not None:
            # Offset
            offset = pagination_index * 50

            # Final query
            final_query = default_query + " " + order_query

            # Search products without pagination
            search_products_without_pagination = self.db.execute(final_query, *params)

            # Number of products
            number_of_products = len(search_products_without_pagination)

            # Final query with limit and offset
            final_query = final_query + f" LIMIT 50 OFFSET {offset}"

            # Search products with pagination
            search_products_with_pagination = self.db.execute(final_query, *params)

            return (search_products_with_pagination, number_of_products)
        
        # Incremenent sub category filters to default query
        final_query = default_query + " " + order_query

        # Ensure search has limit
        if limit is not None:
            final_query += f" LIMIT {limit}"
        
        # Query products
        search_products = self.db.execute(final_query, *params)

        # Return search results
        return search_products
    
    def query_search_my_services_with_filters(self, filters: dict) -> list:
        """ Search services based in filters """

        # Search filters
        description_bar_code_filter = filters["description_bar_code_filter"]
        order_by_filter = filters["order_by_filter"]
        asc_desc_filter = filters["asc_desc_filter"]

        # Query servives with filters
        search_services = self.db.execute(f""" SELECT "Service" AS type, "--" as category, "--" as sub_category, services.id, services_basic.description, services_basic.bar_code, services_financial.cost_price, services_financial.sell_price, services_financial.margin_percentage, services_financial.unity_m
                                       FROM services
                                       INNER JOIN services_financial
                                       ON services.id = services_financial.service_id
                                       INNER JOIN services_basic
                                       ON services_financial.service_id = services_basic.service_id
                                       WHERE services_basic.description LIKE ? AND services.company_id = ?
                                       ORDER BY {order_by_filter} {asc_desc_filter} LIMIT 5
                                       """, "%" + description_bar_code_filter + "%", self.company_id)

        # Return searched services
        return search_services
    
    def query_product_services_associated(self, product_id: str) -> list:
        """ Query services associated with product requested by user """

        # Query services associated
        services = self.db.execute("""SELECT services.id, services_basic.description, services_products.stock, services_basic.bar_code, services_financial.cost_price, services_financial.sell_price,
                                    services_financial.margin_percentage
                                    FROM services
                                    INNER JOIN services_basic
                                    ON services.id = services_basic.service_id
                                    INNER JOIN services_financial
                                    ON services_financial.service_id = services_basic.service_id
                                    INNER JOIN services_products
                                    ON services_basic.service_id = services_products.service_id
                                    WHERE services_products.product_id = ?""", product_id)

        # Return services associated
        return services
    
    def query_product_movements(self, product_id: str, start_date: str, end_date: str, movement_type=None, all_movements=False, pagination_index=None):
        """ Query product movements from products_movements table """

        if all_movements and pagination_index is not None:
            # Offset value
            offset = pagination_index * 25

            # Query movements
            movements = self.db.execute("SELECT * FROM products_movements WHERE product_id = ? AND DATETIME(date) BETWEEN ? AND ? ORDER BY date DESC LIMIT 25 OFFSET ?", product_id, start_date, end_date, offset)
        
        elif movement_type is not None:
            # Query movements
            movements = self.db.execute("SELECT * FROM products_movements WHERE movement_type = ? AND product_id = ? AND DATETIME(date) BETWEEN ? AND ? ORDER BY date ASC", movement_type, product_id, start_date, end_date)
        
        else:
             # Query movements
            movements = self.db.execute("SELECT * FROM products_movements WHERE product_id = ? AND DATETIME(date) BETWEEN ? AND ? ORDER BY date ASC", product_id, start_date, end_date)
        
        # Return movements
        return movements
    
    def query_service_movements(self, service_id: str, start_date: str, end_date: str, movement_type=None, all_movements=False, pagination_index=None):
        """ Query service movements from service_movements table """

        if all_movements and pagination_index is not None:
            # Offset value
            offset = pagination_index * 25

            # Query movements
            movements = self.db.execute("SELECT * FROM services_movements WHERE service_id = ? AND DATETIME(date) BETWEEN ? AND ? ORDER BY date DESC LIMIT 25 OFFSET ?", service_id, start_date, end_date, offset)
        
        elif movement_type is not None:
            # Query movements
            movements = self.db.execute("SELECT * FROM services_movements WHERE movement_type = ? AND service_id = ? AND DATETIME(date) BETWEEN ? AND ? ORDER BY date ASC", movement_type, service_id, start_date, end_date)
        
        else:
             # Query movements
            movements = self.db.execute("SELECT * FROM services_movements WHERE service_id = ? AND DATE(date) BETWEEN ? AND ? ORDER BY date ASC", service_id, start_date, end_date)
        
        # Return movements
        return movements
    
    def query_product_last_movement(self, product_id: str, movement_type: int) -> list:
        """ Query product last movement from products_movements table """

        # Query product last movement
        last_movement = self.db.execute("SELECT id from product_movements WHERE product_id = ? AND movement_type = ? ORDER BY id DESC LIMIT 1", product_id, movement_type)
        
        return last_movement

    def query_all_products_from_order_list(self):
        """ Query all products from temp_order_list """

        # Query all products from order list
        order_products = self.db.execute("SELECT * FROM temp_order_list WHERE company_id = ? ORDER BY description", self.company_id)

        return order_products

    def query_products_from_order_list_with_pagination(self, pagination_index=None):
        """ Query products from order list with offset """

        if pagination_index is not None:

            offset = int(pagination_index) * 20

            # Query  products from order list
            order_products = self.db.execute("SELECT * FROM temp_order_list WHERE company_id = ? ORDER BY description LIMIT 20 OFFSET ?", self.company_id, offset)
        else:
            # Query sum of all products in order list
            order_products = self.db.execute("SELECT * FROM temp_order_list WHERE company_id = ?", self.company_id)

        # Return ordr products
        return order_products
    
    def query_order_total(self) -> float:
        """ Query calculated order total from temp_order_list """

        # Query order total
        order_total = self.db.execute("SELECT SUM(cost_price * quantity) AS order_total FROM temp_order_list WHERE company_id = ?", self.company_id)

        order_total = order_total[0]["order_total"]

        # Return order total
        return order_total if order_total is not None else 0
    
    def query_all_expenses(self) -> list:
        """ Query all user expenses from expenses table """

        # Query expenses
        expenses = self.db.execute("SELECT * FROM expenses WHERE company_id = ?", self.company_id)

        # Return user expenses
        return expenses
    
    def query_date_expenses(self, month: int, year: int) -> list:
        """ Query searched date expenses from expenses table """

        # Query for date expenses data
        date_expenses = self.db.execute("SELECT SUM(total) as total, expense_id, insert_year, insert_month, insert_day FROM expenses WHERE expense_month = ? AND expense_year = ? AND company_id = ? GROUP BY expense_id", month, year, self.company_id)

        # Return date expenses data
        return date_expenses

    def query_workers(self) -> list:
        """ Query company workers from workers table """

        # Query company workers
        workers = self.db.execute("SELECT * FROM workers WHERE company_id = ?", self.company_id)

        # Return workers
        return workers
    
    def query_worker(self, worker_id: str):
        """ Query worker information from workers table """

        # Query worker information
        worker_data = self.db.execute("""
                                      SELECT workers.fullname, workers.adress, workers.born_date, workers.contact, workers.section, workers.role,
                                      workers.workload_day, workers.workload_week, workers.base_salary, workers.id, workers.worker_number
                                      FROM workers WHERE id = ?""", worker_id)
       
        # Return worker data
        return worker_data
    
    def query_worker_absences(self, worker_id: str, absences_date_to_consult=None) -> list:
        """ Query all worker abstences """

        # Ensure that has date to consult in query
        if absences_date_to_consult is not None:
            start_date = absences_date_to_consult[0]
            end_date = absences_date_to_consult[1]

            # Query worker absences with absences dates to consult
            worker_absences = self.db.execute("SELECT * FROM workers_absences WHERE worker_id = ? AND (start_date BETWEEN ? AND ?) OR (end_date BETWEEN ? AND ?)", worker_id, start_date, end_date, start_date, end_date)   
        else:
            # Query all workers
            worker_absences = self.db.execute("SELECT * FROM workers_absences WHERE worker_id = ?", worker_id)

        # Return all workers
        return worker_absences
    
    def query_worker_benefits(self, worker_id: str, benefits_date_to_consult=None) -> list:
        """ Query all worker abstences """

        # Ensure that has date to consult in query
        if benefits_date_to_consult is not None:
            # Start and end date to search
            start_date = benefits_date_to_consult[0]
            end_date = benefits_date_to_consult[1]

            # Query worker absences with absences dates to consult
            worker_benefits = self.db.execute("SELECT * FROM workers_benefits WHERE worker_id = ? AND date BETWEEN ? AND ?", worker_id, start_date, end_date)   
        else:
            # Query all workers
            worker_benefits = self.db.execute("SELECT * FROM workers_benefits WHERE worker_id = ?", worker_id)

        # Return all workers
        return worker_benefits
    
    def query_inventories(self) -> list:
        """ Query company inventories from inventories table """

        # Query inventories
        inventories = self.db.execute("SELECT * FROM inventories WHERE company_id = ? ORDER BY created_date DESC", self.company_id)

        # Return inventories
        return inventories

    def query_open_inventories(self) -> list:
        """ Query company open inventories from inventories table """

        # Open inventories
        open_inventories = self.db.execute("SELECT * FROM inventories WHERE status != 'closed' AND inventories.company_id = ?", self.company_id)

        # Return open inventories
        return open_inventories
    
    def query_inventory(self, inventory_id: str) -> list:
        """ Query inventory all information from inventories table """

        # Query inventory
        inventory = self.db.execute("SELECT * FROM inventories WHERE id = ?", inventory_id)

        return inventory
    
    def query_inventory_products(self, inventory_id, pagination_index=None or int, all_to_search=False) -> list:
        """ Query inventory information from inventories_products table using off set or query all"""

        # Default query
        default_query = """SELECT products.id, products_basic.bar_code, products_basic.description, inventories_products.real_stock, inventories_products.cost_price,
                                                inventories_products.stock_counted, inventories_products.status,
                                                inventories_products.stock_counted - inventories_products.real_stock AS stock_diff, (inventories_products.stock_counted - inventories_products.real_stock) * inventories_products.cost_price AS stock_diff_value
                                                FROM products INNER JOIN products_basic
                                                ON products.id = products_basic.product_id
                                                INNER JOIN products_financial
                                                ON products_basic.product_id = products_financial.product_id
                                                INNER JOIN inventories_products
                                                ON products.id = inventories_products.product_id 
                                                WHERE inventories_products.inventory_id = ? ORDER by products_basic.description ASC """

        if all_to_search:
            # Query all products
            all_inventory_products = self.db.execute(default_query, inventory_id)

            return all_inventory_products

        default_query += "LIMIT 25 OFFSET ?"

        # Offset 
        offset = pagination_index * 25

        # Query inventory info
        inventory_products = self.db.execute(default_query, inventory_id, offset)

        # All inventory products count
        count_inventory_products = self.db.execute("""SELECT COUNT(products.id) AS products_count
                                                        FROM products INNER JOIN products_basic
                                                        ON products.id = products_basic.product_id
                                                        INNER JOIN products_financial
                                                        ON products_basic.product_id = products_financial.product_id
                                                        INNER JOIN inventories_products
                                                        ON products.id = inventories_products.product_id
                                                        WHERE inventories_products.inventory_id = ?
                                                        """, inventory_id)
        
        count_inventory_products = count_inventory_products[0]["products_count"]

        # Return inventory_info
        return inventory_products, count_inventory_products
    
    def query_inventory_diff_and_total(self, inventory_id: str) -> list: 
        """ Query inventory global diff and total """

        # Query inventory diff and total
        inventory_diff_and_total = self.db.execute("""SELECT SUM(stock_counted - real_stock) AS stock_diff,
                                                    SUM((stock_counted - real_stock) * inventories_products.cost_price) AS stock_diff_value
                                                    FROM inventories_products
                                                    WHERE inventory_id = ?""", inventory_id)
        print(inventory_diff_and_total)

        # Return inventory diff and total
        return inventory_diff_and_total
    
    def query_recount_inventory_products(self, inventory_id: str, pagination_index=None ):
        """ Query recount products from inventories_products table """

        # Offset
        offset = pagination_index * 25

        # Query recount products
        recount_products = self.db.execute("""SELECT products.id, products_basic.bar_code, products_basic.description, inventories_products.stock_counted
                                            FROM products 
                                            INNER JOIN products_basic
                                            ON products.id = products_basic.product_id
                                            INNER JOIN inventories_products
                                            ON products_basic.product_id = inventories_products.product_id 
                                            WHERE inventories_products.status = 'recount'
                                            AND inventories_products.inventory_id = ? LIMIT 25 OFFSET ?""", inventory_id, offset)
        
        # Query recount products count
        count_recount_products = self.db.execute("""SELECT COUNT(products.id) AS count
                                                    FROM products 
                                                    INNER JOIN products_basic
                                                    ON products.id = products_basic.product_id
                                                    INNER JOIN inventories_products
                                                    ON products_basic.product_id = inventories_products.product_id 
                                                    WHERE inventories_products.status = 'recount'
                                                    AND inventories_products.inventory_id = ?""", inventory_id )

        # Return recount products
        return recount_products, count_recount_products[0]["count"]
    
    def query_closed_inventories(self, month=None, year=None):
        """ Query closed inventories """

        if month is None and year is None:
            # Query closed inventories
            closed_inventories = self.db.execute("SELECT * FROM inventories WHERE status = 'closed' AND company_id = ?", self.company_id)
        else:
            # Query closed inventories with month and year
            closed_inventories = self.db.execute("SELECT * FROM inventories WHERE status = 'closed' AND year_created = ? AND month_created = ? AND company_id = ?", year, month, self.company_id)

        # Return closed inventories
        return closed_inventories

    def query_product_inventories(self, product_id: str, status=None or str) -> list:
        """ Query product inventories """

        if status == "open":
            product_inventories = self.db.execute("SELECT * FROM inventories_products WHERE product_id = ? AND (status = 'not_counted' OR status = 'recount')", product_id)

            return product_inventories
        
        # Query inventories
        product_inventories = self.db.execute("SELECT * FROM inventories_products WHERE product_id = ?", product_id)

        # Return inventories
        return product_inventories
     
    def query_company_sales(self, start_date: str, end_date: str) -> float:
        """ Query company sales from companies_sales table """

        # Query company sales
        sales = self.db.execute("SELECT IFNULL(SUM(total),0) as sales FROM companies_sales WHERE company_id = ? AND date BETWEEN ? AND ?", self.company_id, start_date, end_date)

        sales = sales[0]["sales"]

        return sales
    
    def query_company_wastes(self, start_date: str, end_date: str) -> float:
        """ Query company wastes from companies_wastes table """

        # Query company wastes
        wastes = self.db.execute("SELECT IFNULL(SUM(total),0) as wastes FROM companies_wastes WHERE date BETWEEN ? AND ? AND company_id = ?", start_date, end_date, self.company_id)

        # Query products benefits
        benefits = self.query_products_benefits(start_date, end_date)

        print("WASTES")
        print(wastes)

        return wastes[0]["wastes"] - benefits

    def query_product_sales(self, start_date: str, end_date: str, product_id: str) -> float:
        """ Query product sales from products_sales table and return """

        # Query product sales
        product_sales = self.db.execute("""SELECT IFNULL(SUM(total),0) AS sales
                                        FROM products_sales 
                                        WHERE product_id = ?
                                        AND date BETWEEN ? AND ?""", product_id, start_date, end_date)
        
        product_sales = product_sales[0]["sales"]

        return product_sales
    
    def query_service_sales(self, start_date, end_date, product_id):
        """ Query product sales from products_sales table and return """

        # Query product sales
        product_sales = self.db.execute("""SELECT IFNULL(SUM(total),0) AS sales
                                        FROM services_sales 
                                        WHERE service_id = ?
                                        AND date BETWEEN ? AND ?""", product_id, start_date, end_date)
        
        product_sales = product_sales[0]["sales"]

        return product_sales

    def query_product_wastes(self, start_date: str, end_date: str, product_id: int) -> float:
        """ Query product wastes products_wastes table and return"""

        # Query product wastes
        wastes = self.db.execute("SELECT IFNULL(SUM(total),0) as wastes FROM products_wastes WHERE date BETWEEN ? AND ? AND product_id = ?", start_date, end_date, product_id)

        wastes = wastes[0]["wastes"]

        return wastes
    
    def query_service_wastes(self, start_date, end_date, product_id):
        """ Query service wastes from service_identified_wastes table """

        # Query service wastes
        wastes = self.db.execute("SELECT IFNULL(SUM(total),0) as wastes FROM services_identified_wastes WHERE date BETWEEN ? AND ? AND service_id = ?", start_date, end_date, product_id)

        # Get wastes value
        wastes = wastes[0]["wastes"]

        return wastes

    def query_most_profit_product(self, start_date, end_date):
        """ Query most prodit product and return """

        # Query most profit product description and value
        params = (start_date, end_date, start_date, end_date, self.company_id)

        # Query product profit
        most_profit_product = self.db.execute("""SELECT products_basic.description as product_description,
                                                    (SELECT IFNULL(SUM(products_profit.total),0)
                                                    FROM products_profit
                                                    WHERE products_profit.date BETWEEN ? AND ?
                                                    AND products_profit.product_id = products_basic.product_id) 
                                                    -
                                                    
                                                    (SELECT IFNULL(SUM(products_wastes.total), 0)
                                                    FROM products_wastes
                                                    WHERE products_wastes.date BETWEEN ? AND ?
                                                    AND products_wastes.product_id = products_basic.product_id) AS product_profit
                                                FROM products_basic
                                                WHERE products_basic.product_id IN (SELECT id FROM products where company_id = ?)
                                                GROUP BY products_basic.product_id
                                                ORDER BY product_profit DESC LIMIT 1""", *params)

        return most_profit_product
    
    def query_most_profit_service(self, start_date, end_date):
        """ Query most profit service and return """

        # Query most profit service description and value
        most_profit_service = self.db.execute("""SELECT 
                                                    IFNULL(SUM(total),0) AS service_profit, IFNULL(services_basic.description, '--') AS service_description
                                                FROM 
                                                    services_profit
                                                INNER JOIN 
                                                    services_basic
                                                ON 
                                                    services_profit.service_id = services_basic.service_id  
                                                WHERE
                                                    services_profit.service_id IN (SELECT id from services WHERE company_id = ?)
                                                AND
                                                    date BETWEEN ? AND ?
                                                GROUP BY
                                                    services_profit.service_id
                                                ORDER BY
                                                    service_profit DESC LIMIT 1""", self.company_id, start_date, end_date)

        return most_profit_service
    
    def query_most_wasted_product(self, start_date, end_date):
        """ Query most wasted product """

        # Query most wasted product description and value
        most_wasted_product = self.db.execute("""SELECT IFNULL(SUM(products_wastes.total),0) AS waste, IFNULL(products_basic.description, '--') AS product_description
                                                 FROM products_wastes
                                                 INNER JOIN products_basic
                                                 ON products_wastes.product_id = products_basic.product_id  
                                                 WHERE products_wastes.date BETWEEN ? AND ?
                                                 AND products_wastes.product_id IN (SELECT id FROM products WHERE company_id = ?)
                                                 GROUP BY products_wastes.product_id
                                                 ORDER BY waste DESC LIMIT 1
                                              """, start_date, end_date, self.company_id)
        
        return most_wasted_product
    
    def query_most_wasted_service(self, start_date, end_date):
        """ Query most wasted service """

        # Query most wasted product description and value
        most_wasted_service = self.db.execute("""SELECT IFNULL(SUM(services_identified_wastes.total),0) AS waste, IFNULL(services_basic.description, '--') AS service_description
                                                 FROM services_identified_wastes
                                                 INNER JOIN services_basic
                                                 ON services_identified_wastes.service_id = services_basic.service_id  
                                                 WHERE services_identified_wastes.date BETWEEN ? AND ?
                                                 AND services_identified_wastes.service_id IN (SELECT id FROM services WHERE company_id = ?) 
                                                 GROUP BY services_identified_wastes.service_id
                                                 ORDER BY waste DESC LIMIT 1
                                              """, start_date, end_date, self.company_id)
        
        return most_wasted_service
    
    def query_company_waste_motives_and_values(self, start_date, end_date):
        """ Query company wastes motives and values with start and end date """

        # Parameters
        params = (start_date, end_date, self.company_id)

        # Query identified wastes motives and values    
        motives_and_values = self.db.execute("""SELECT IFNULL(SUM(total),0) as total, motive 
                                                FROM products_identified_wastes
                                                WHERE date
                                                BETWEEN ? AND ?
                                                AND product_id IN (SELECT id from products WHERE company_id = ?)
                                                GROUP by motive""", *params)
        
        # Query non identified waste and set 'Non identified waste' as motive to match identified wastes query
        non_identified_wastes = self.db.execute("""SELECT IFNULL(SUM(total),0) as total, 'Non identified waste' AS motive
                                                   FROM products_non_identified_wastes
                                                   WHERE date 
                                                   BETWEEN ? AND ? 
                                                   AND product_id IN (SELECT id from products WHERE company_id = ?)""", *params)
        
        # Merge two lists
        motives_and_values.extend(non_identified_wastes)
        
        return motives_and_values
    
    def query_product_waste_motives_and_values(self, start_date, end_date, product_id):
        """ Query product waste motives and respective values with start and end date and return"""

        # Parameters
        params = (start_date, end_date, product_id)

        # Query motives and values from products_identified_wastes
        motives_and_values = self.db.execute("""SELECT IFNULL(SUM(total),0) as total, motive FROM products_identified_wastes
                                                WHERE date
                                                BETWEEN ? AND ?
                                                AND product_id = ?
                                                GROUP by motive""", *params)
        
        # Query products_non_identified_wastes
        non_identified_wastes = self.db.execute("""SELECT IFNULL(SUM(total),0) as total, 'Non identified waste' AS motive
                                                   FROM products_non_identified_wastes
                                                   WHERE date BETWEEN ? AND ? 
                                                   AND product_id = ?""", *params)
        
        motives_and_values.extend(non_identified_wastes)
        

        return motives_and_values
    
    def query_service_waste_motives_and_values(self, start_date, end_date, service_id):
        """ Query product waste motives and respective values with start and end date and return"""

        params = (start_date, end_date, service_id)

        # Query motives and values from products_identified_wastes
        waste_motives_and_values = self.db.execute("""SELECT IFNULL(SUM(total),0) as total, motive FROM services_identified_wastes
                                                WHERE date
                                                BETWEEN ? AND ?
                                                AND service_id = ?
                                                GROUP by motive""", *params)
        

        return waste_motives_and_values
    
    def query_sales_wastes_dates(self):
        """ Query company movements dates and return """

        # Query movements dates
        movements_dates = self.db.execute("""SELECT DISTINCT companies_sales.date FROM companies_sales
                                            LEFT JOIN products_sales
                                            ON companies_sales.date = products_sales.date
                                            WHERE product_id IN (SELECT id from products WHERE company_id = ?) 
                                            GROUP by companies_sales.date ORDER BY companies_sales.date DESC""", self.company_id)

        # Return movements dates
        return movements_dates

    def query_movements_dates(self, movements=None):
        """ Query movements dates """

        if movements is None:
            dates = self.db.execute(""" SELECT DISTINCT DATE(date) AS date FROM products_movements WHERE product_id IN (SELECT id FROM products WHERE company_id = ?)""", self.company_id)
        else:
            # Create placeholders
            print(movements)
            placeholders = " ,".join("?" for _ in movements)

            dates = self.db.execute(f""" SELECT DISTINCT DATE(date) AS date FROM products_movements WHERE movement_type IN ({placeholders}) AND  product_id IN (SELECT id FROM products WHERE company_id = ?)""", *movements, self.company_id)
        return dates

    def query_company_sales_movement_total(self, start_time, end_time, start_date, end_date):
        """ Query company sales movements total from products_movements table """

        # Query sales movements total
        sales_movements_total = self.db.execute("""
                                                SELECT IFNULL(SUM(total),0) AS sales
                                                FROM products_movements 
                                                WHERE movement_type = 107
                                                AND DATE(date) BETWEEN ? AND ?
                                                AND TIME(date) BETWEEN ? AND ?
                                                AND product_id IN (SELECT id from products WHERE company_id = ?)""", start_date, end_date, start_time, end_time, self.company_id)


        sales_movements_total = sales_movements_total[0]["sales"]

        return sales_movements_total
    
    def query_product_sales_movement_total(self, start_time, end_time, start_date, end_date, product_id):
        """ Query product sales movements total from products_movements table """

        sales_movements_total = self.db.execute("""
                                                SELECT IFNULL(SUM(total),0) AS sales
                                                FROM products_movements 
                                                WHERE movement_type = 107
                                                AND DATE(date) BETWEEN ? AND ?
                                                AND TIME(date) BETWEEN ? AND ?
                                                AND product_id = ?""",  start_date, end_date, start_time, end_time,product_id)
        
        sales_movements_total = sales_movements_total[0]["sales"]

        return sales_movements_total
    
    def query_service_sales_movement_total(self, start_time, end_time, start_date, end_date, service_id):
        """ Query servive sales movements total from services_movements table """

        sales_movements_total = self.db.execute("""
                                                SELECT IFNULL(SUM(total),0) AS sales
                                                FROM services_movements 
                                                WHERE movement_type = 106
                                                AND DATE(date) BETWEEN ? AND ?
                                                AND TIME(date) BETWEEN ? AND ?
                                                AND service_id = ?""",  start_date, end_date, start_time, end_time,service_id)
        
        sales_movements_total = sales_movements_total[0]["sales"]

        return sales_movements_total

    def query_products_with_most_units_sell(self, start_date, end_date):
        """ Query top 10 products with mosts units sell """

        # Query products units sell
        products_units_sell = self.db.execute("""SELECT SUM(units_sell) as units_sell, products_basic.description as product_description
                                      FROM products_sales
                                      INNER JOIN products_basic
                                      ON products_sales.product_id = products_basic.product_id
                                      WHERE products_sales.product_id IN (SELECT id from products WHERE company_id = ?)
                                      AND products_sales.date BETWEEN ? AND ?
                                      GROUP by product_description ORDER BY units_sell DESC LIMIT 10""", self.company_id, start_date, end_date)

        return products_units_sell
    
    def query_services_with_most_units_sell(self, start_date, end_date):
        """ Query top 10 products with mosts units sell """

        # Query products units sell
        products_units_sell = self.db.execute("""SELECT SUM(units_sell) as units_sell, services_basic.description as service_description
                                      FROM services_sales
                                      INNER JOIN services_basic
                                      ON services_sales.service_id = services_basic.service_id
                                      WHERE services_sales.service_id IN (SELECT id from services WHERE company_id = ?)
                                      AND services_sales.date BETWEEN ? AND ?
                                      GROUP by service_description ORDER BY units_sell DESC LIMIT 10""", self.company_id, start_date, end_date)

        return products_units_sell
    
    def query_product_units_sell(self, start_date, end_date, product_id):
        """ Query product units sell """

        product_units_sell = self.db.execute("""SELECT IFNULL(SUM(products_sales.units_sell),0) as units_sell, products_basic.description as product_description
                                      FROM products_sales
                                      INNER JOIN products_basic
                                      ON products_sales.product_id = products_basic.product_id
                                      WHERE products_sales.product_id = ?
                                      AND products_sales.date BETWEEN ? AND ?""", product_id, start_date, end_date)
        
        return product_units_sell
    
    def query_service_units_sell(self, start_date, end_date, service_id):
        """ Query service units sell """

        service_units_sell = self.db.execute("""SELECT IFNULL(SUM(services_sales.units_sell), 0) as units_sell
                                      FROM services_sales
                                      INNER JOIN services_basic
                                      ON services_sales.service_id = services_basic.service_id
                                      WHERE services_basic.service_id = ?
                                      AND services_sales.date BETWEEN ? AND ?""", service_id, start_date, end_date)
        
        
        if service_units_sell is None:
            service_units_sell = 0
        
        return service_units_sell
    
    def query_product_profit(self, start_date, end_date, product_id):
        """ Query product profit from products_profit table and return """

        # Parameters
        params = (start_date, end_date, product_id, start_date, end_date, product_id)

        # Query product profit
        product_profit = self.db.execute("""SELECT
                                                (SELECT IFNULL(SUM(products_profit.total),0)
                                                FROM products_profit
                                                WHERE products_profit.date BETWEEN ? AND ?
                                                AND products_profit.product_id = ?) 
                                                -
                                                
                                                (SELECT IFNULL(SUM(products_wastes.total), 0)
                                                FROM products_wastes
                                                WHERE products_wastes.date BETWEEN ? AND ?
                                                AND products_wastes.product_id = ?) AS product_profit""", *params)
                
        # Get product profit value
        product_profit = product_profit[0]["product_profit"]

        return product_profit
    
    def query_company_profit(self, start_date: str, end_date: str) -> float:
        """ Query company profit """

        # Query products profit 
        products_profit = self.db.execute("SELECT IFNULL(SUM(total), 0) AS profit FROM products_profit WHERE date BETWEEN ? AND ? AND product_id IN (SELECT id from products WHERE company_id = ?)", start_date, end_date, self.company_id)
        
        # Query services profit
        services_profit = self.db.execute("SELECT IFNULL(SUM(total), 0) AS profit FROM services_profit WHERE date BETWEEN ? AND ? AND service_id IN (SELECT id from services WHERE company_id = ?)", start_date, end_date, self.company_id)
        
        # Return sum of products with services profit
        return products_profit[0]["profit"] + services_profit[0]["profit"]

    def query_service_profit(self, start_date, end_date, product_id):
        """ Query service profit from services_profit table and return """

        # Query service profit
        service_profit = self.db.execute("""SELECT IFNULL(SUM(services_profit.total - services_identified_wastes.total),0) as service_profit
                                                FROM services_profit
                                                INNER JOIN services_identified_wastes
                                                ON services_profit.service_id = services_identified_wastes.service_id
                                                WHERE services_profit.date BETWEEN ? AND ?
                                                AND services_profit.service_id = ?""", start_date, end_date, product_id)
        
        # Get service profit value
        service_profit = service_profit[0]["service_profit"]

        return service_profit
    
    def query_products_benefits(self, start_date: str, end_date: str) -> float:
        """ Query products benefits from products_benefits table """

        products_benefits = self.db.execute("SELECT IFNULL(SUM(total), 0) AS products_benefits FROM products_regularization_benefits WHERE date BETWEEN ? AND ? AND product_id IN (SELECT id FROM products WHERE company_id = ?)", start_date, end_date, self.company_id)

        products_benefits = products_benefits[0]["products_benefits"]

        return products_benefits
    
    def query_products_by_stock(self, search_type: str, pagination_index=None) -> list:
        """ Query products by stock type"""

        # Default query
        query = """SELECT * FROM products
                   INNER JOIN products_basic
                   ON products.id = products_basic.product_id
                   INNER JOIN products_financial
                   ON products.id = products_financial.product_id
                   WHERE products.company_id = ? 
                   AND products_financial.stock """

        # Ensure which type of search
        if search_type == "negative_stock":
            query += "< 0"
        elif search_type == "null_stock":
            query += "= 0"
        else:
            query +="> 0"

        if pagination_index is not None:
            # Get offset
            offset = pagination_index * 25

            query += f" LIMIT 25 OFFSET {offset}"

        # Query products
        products = self.db.execute(query, self.company_id)

        return products
    
    def query_products_without_sales_in_last_fifteen_days(self, start_date: str, end_date: str, pagination_index=None) -> list:
        """ Query products without sales in last fifteen days """

        # Query all products
        all_products = self.query_all_products()

        # Get products ids
        ids = [product["id"] for product in all_products]

        query = """SELECT IFNULL(SUM(products_sales.total), 0) AS sales, products_basic.description, products_basic.bar_code, products_financial.stock
                                    FROM products_basic
                                    LEFT JOIN products_sales
                                    ON products_sales.product_id = products_basic.product_id
                                    AND products_sales.date BETWEEN ? AND ?
                                    INNER JOIN products_financial
                                    ON products_basic.product_id = products_financial.product_id
                                    WHERE products_basic.product_id IN (SELECT id FROM products WHERE company_id = ?)
                                    GROUP BY products_basic.product_id
                                    HAVING sales = 0
                                    ORDER BY products_basic.description ASC
                """
        
        if pagination_index is not None:
            # Offset
            offset = pagination_index * 25

            query += f" LIMIT 25 OFFSET {offset}"

        # Query products
        products = self.db.execute(query, start_date, end_date, self.company_id)
        
        print(len(ids))
        print(len(products))

        return products
    
    def query_scanned_bar_code(self, bar_code):
        """ Query product or service for bar code """

        # Search for services
        scanned_info = self.db.execute("""SELECT services_basic.description, services_basic.bar_code, services_financial.sell_price, services_financial.unity_m, services.id, "Service" as type
                                  FROM services_basic
                                  INNER JOIN services_financial
                                  ON services_basic.service_id = services_financial.service_id
                                  INNER JOIN services
                                  ON services_financial.service_id = services.id
                                  WHERE services.company_id = ?
                                  AND services_basic.bar_code LIKE ?""", self.company_id, bar_code)
        # If no results in services search for product
        if not scanned_info:
            # Search for product
            scanned_info = self.db.execute("""SELECT products_basic.description, products_basic.bar_code, products_financial.sell_price, products_financial.unity_m, products.id, "Product" as type
                                            FROM products_basic
                                            INNER JOIN products_financial
                                            ON products_basic.product_id = products_financial.product_id
                                            INNER JOIN products
                                            ON products_financial.product_id = products.id
                                            WHERE products.company_id = ?
                                            AND products_basic.bar_code LIKE ?""", self.company_id, bar_code)

        # Return service info
        return scanned_info

    def update_product_stock(self, product_id: int, stock: float, movement_type: str):
        """ Update products stock """
        # Ensure which movement type is
        if movement_type == "order_entry" or movement_type == "sale_refund":
            # Incremenent product stock in products table
            self.db.execute("UPDATE products_financial set stock = stock + ? WHERE product_id = ?", round(stock, 3), product_id )
        elif movement_type == "regularize" or movement_type == "inventory":
            # Update product stock
            self.db.execute("UPDATE products_financial SET stock = ? WHERE product_id = ?", round(stock, 3), product_id)
        else:
            # Decrement stock waste
            self.db.execute("UPDATE products_financial SET stock = stock - ? WHERE product_id = ?", round(stock, 3), product_id)

    def update_product_basic(self, product_id, description, bar_code, category, sub_category):
        """ Update product basic information """

        self.db.execute("UPDATE products_basic SET description = ?, bar_code = ?, category = ?, sub_category = ? WHERE product_id = ?", description, bar_code, category, sub_category, product_id)

    def update_product_financial(self, product_id, cost_price, sell_price, margin_percentage, unity_m):
        """ Update product financial table """

        # Update product
        self.db.execute("UPDATE products_financial SET cost_price = ?, sell_price = ?, margin_percentage = ?, unity_m = ? WHERE product_id = ?", round(cost_price, 2), round(sell_price, 2), round(margin_percentage, 2), unity_m, product_id)
    
    def update_product_sales(self, product_id, total, units, date, incre=False):
        """ Update product sales in products_sales table """

        # Ensure user want to decrement sales or decrement sales
        if not incre:
            update_query = "total = total - ?, units_sell = units_sell - ?"
        
        else:
            update_query = "total = total + ?, units_sell = units_sell + ?"

        # Update product sales
        self.db.execute(f"UPDATE products_sales SET {update_query} WHERE product_id = ? AND date = ?", round(total, 2), round(units, 3), product_id, date)

    
    def update_product_profit(self, product_id, total, date, incre=False):
        """ Update product profit in products_profit table """
        
        # Ensure user want to decrement sales or decrement sales
        if not incre:
            update_query = "total = total - ?"
        
        else:
            update_query = "total = total + ?"

        # Update product sales
        self.db.execute(f"UPDATE products_profit SET {update_query} WHERE product_id = ? AND date = ?", round(total, 2), product_id, date)


    def update_service_basics(self, service_id, service_description):
        """ Update services basics table """

        # Update service
        self.db.execute("UPDATE services_basic SET description = ? WHERE service_id = ?", service_description, service_id)

    def update_service_financial(self, service_id, cost_price, sell_price, margin_percentage):
        """ Update services financial table """

        # Update service
        self.db.execute("UPDATE services_financial SET cost_price = ?, sell_price = ?, margin_percentage = ? WHERE service_id = ?", round(cost_price, 2), round(sell_price, 2), round(margin_percentage, 2), service_id)

    def update_service_products_and_stocks(self, service_id, service_products_and_stocks):
        """ Update services_products table """
    
        # Delete products from service_products
        self.db.execute("DELETE FROM services_products WHERE service_id = ?", service_id)

        # Insert news products in services_products table
        for product in service_products_and_stocks:
            self.db.execute("INSERT INTO services_products (service_id, stock, product_id) VALUES (?,?,?)", service_id, float(round(product["stock_associated"], 3)), product["product"])

    def update_service_sales(self, service_id, total, units, date, incre=False):
        """ Update service sales in products_sales table """

        # Ensure user want to decrement sales or decrement sales
        if not incre:
            update_query = "total = total - ? AND units_sell = units_sell - ?"
        
        else:
            update_query = "total = total + ? AND units_sell = units_sell + ?"

        # Update product sales
        self.db.execute(f"UPDATE services_sales SET {update_query} WHERE service_id = ? AND date = ?", round(total, 2), round(units, 3), service_id, date)

    
    def update_service_profit(self, service_id, total, date, incre=False):
        """ Update service profit in products_profit table """
        
        # Ensure user want to decrement sales or decrement sales
        if not incre:
            update_query = "total = total - ?"
        
        else:
            update_query = "total = total + ?"

        # Update product sales
        self.db.execute(f"UPDATE services_profit SET {update_query} WHERE service_id = ? AND date = ?", round(total, 2), service_id, date)

    def update_company_sales(self, date, total, units, incre=False):
        """ Update company sales from companies_sales """

        # Ensure user want to decrement sales or decrement sales
        if not incre:
            update_query = "total = total - ?, units_sell = units_sell - ?"
        
        else:
            update_query = "total = total + ?, units_sell = units_sell + ?"

         # Update product sales
        self.db.execute(f"UPDATE companies_sales SET {update_query} WHERE date = ? AND company_id = ?", round(total, 2), round(units, 3), date, self.company_id)

    
    def update_company_profit(self, date, total, incre=False):
        """ Update company profit in companies_profit table """
        
        # Ensure user want to decrement sales or decrement sales
        if not incre:
            update_query = "total = total - ?"
        
        else:
            update_query = "total = total + ?"

        # Update product sales
        self.db.execute(f"UPDATE companies_profit SET {update_query} WHERE date = ? AND company_id = ?", round(total, 2), date, self.company_id)

    
    def update_worker_data(self, worker_id, worker_fullname, worker_adress, worker_contact, worker_born_date, worker_section, worker_role, worker_workload_day, worker_workload_week, worker_base_salary):
        """ Update worker data """

        # Updatw worker data
        self.db.execute("""UPDATE workers SET fullname = ?,
                        adress = ?,
                        contact = ?,
                        born_date = ?,
                        section = ?,
                        role = ?,
                        workload_day = ?,
                        workload_week = ?,
                        base_salary = ? WHERE id = ? AND company_id = ?""",
                        worker_fullname, worker_adress, worker_contact, worker_born_date, worker_section, worker_role, worker_workload_day, worker_workload_week, worker_base_salary, worker_id, self.company_id)

    def update_product_inventory_count(self, inventory_id, product_id, count):
        """ Insert product count in inventories_products """

        # Insert count
        self.db.execute("UPDATE inventories_products SET stock_counted = ? WHERE inventory_id = ? AND product_id = ?", count, inventory_id, product_id)

    def update_inventory_status(self, inventory_id, status):
        """ Update inventory status in 'inventories_products' table """

        # Update inventory status
        self.db.execute("UPDATE inventories SET status = ? WHERE id = ?", status, inventory_id)

    def update_inventory_products_status(self, inventory_id, product_ids, status):
        """ Update products status in inventories_products table """

        # Update products status
        self.db.execute("UPDATE inventories_products SET status = ? WHERE product_id IN (?) AND inventory_id = ?", status, product_ids, inventory_id)

    def query_all_products_from_temp_register_list(self):
        """ Return all user products from 'temp_register_list' table """

        # Query all user products
        products_from_temp_register_list = self.db.execute("SELECT * FROM temp_register_list WHERE company_id = ?", self.company_id)

        # Return all user products in temp_register_list table
        return products_from_temp_register_list
    
    def insert_product_in_temp_register_list(self, description, bar_code, unity_m, category, sub_category, cost_price, sell_price, margin_percentage, quantity):
        """ Insert product information in temp_register_list table """

        # Params
        params = ( description, bar_code, unity_m, category, sub_category, cost_price, sell_price, margin_percentage, quantity, self.company_id)
        
        # Insert product information in temp_register_list table
        self.db.execute("INSERT INTO temp_register_list (description, bar_code, unity_m, category, sub_category, cost_price, sell_price, margin_percentage, stock, company_id) VALUES (?,?,?,?,?,?,?,?,?,?)", *params)
        
    def insert_products(self):
        """ Query products in 'temp_register_list' table and insert in products table """
        
        # Query products in 'temp_register_list'
        products_in_temp_register_list = self.query_all_products_from_temp_register_list()
       
        # Insert all products in 'products' table
        for product in products_in_temp_register_list:
            # Get product info
            description = product["description"]
            bar_code = product["bar_code"]
            unity_m = product["unity_m"]
            category = product["category"]
            sub_category = product["sub_category"]
            cost_price = product["cost_price"]
            sell_price = product["sell_price"]
            margin_percentange = product["margin_percentage"]
            stock = product["stock"]
                
            # Insert product in products table
            self.db.execute("INSERT INTO products (company_id) VALUES (?)", self.company_id)
                    
            # Query products last id inserted by default
            products = self.query_products_ids(limit=1)
                
            # Get id from last inserted row
            product_id = products[0]["id"]

            # Insert product in product_basic table
            self.db.execute("INSERT INTO products_basic (description, bar_code, category, sub_category, product_id) VALUES(?,?,?,?,?)", description, bar_code, category, sub_category, product_id)

            # Insert product in product_financial table
            self.db.execute("INSERT INTO products_financial(stock, cost_price, sell_price, margin_percentage, unity_m, product_id) VALUES(?,?,?,?,?,?)", stock, cost_price, sell_price, margin_percentange, unity_m, product_id)

            # Ensure stock is higher than 0
            if stock > 0:
                # Insert product movement
                self.insert_product_movement(109, stock, datetime.now(), round(stock * cost_price, 2), product_id)

    def insert_service(self, service_description, service_cost_price, service_sell_price, margin_percentage, products_information):
        """ Insert service in services table """

        # Insert service in services table
        self.db.execute("INSERT INTO services (company_id) VALUES (?)", self.company_id)

        # Query services
        services = self.query_services()

        # Service id
        service_id = services[-1]["id"]

        # Create bar code 
        bar_code = 100000 + len(services)

        # Insert service in services_basic table
        self.db.execute("INSERT INTO services_basic (service_id, description, bar_code) VALUES (?,?,?)", service_id, service_description, bar_code)

        # Insert service in services_products table
        for product in products_information:
            self.db.execute("INSERT INTO services_products (service_id, stock, product_id) VALUES (?,?,?)", service_id, float(product.get("stock_associated")), product["product"])

        # Insert service in services_financial tabl
        self.db.execute("INSERT INTO services_financial (cost_price, sell_price, margin_percentage, unity_m, service_id) VALUES (?,?,?,?,?)", service_cost_price, service_sell_price, margin_percentage, "UN", service_id)
        
    def insert_products_in_temp_order_list(self, product_id, description, bar_code, cost_price, sell_price, quantity):
        """ Insert products in temp order list """

        # Parameters
        params = (product_id, description, bar_code, cost_price, sell_price, quantity, self.company_id)

        # Save information in temporary_order_list table
        self.db.execute("INSERT INTO temp_order_list (product_id, description, bar_code, cost_price, sell_price, quantity, company_id) VALUES (?,?,?,?,?,?,?)", *params)
    
    def insert_order(self, order_data, total, date):
        """ Insert order in orders table """

        params = (order_data, round(total, 2), date, self.company_id)

        try:
            # Insert order in orders table
            self.db.execute("INSERT INTO orders (order_data, total, date, company_id) VALUES (?,?,?,?)", *params)
        except ValueError:
            self.db.execute("UPDATE orders SET order_data = order_data + ?, total = total + ? WHERE date = ? AND company_id = ?", *params)

        # Delete all from temp_order_list 
        self.db.execute("DELETE FROM temp_order_list WHERE company_id = ?", self.company_id)

    def insert_product_movement(self, movement_type, stock, date, total, product_id):
        """ Insert movement """

        # Parameters
        params = (round(stock, 3), movement_type, date, round(total, 2), product_id)

        # Insert movement
        self.db.execute("INSERT INTO products_movements (units, movement_type, date, total, product_id) VALUES(?,?,?,?,?)", *params)

    def insert_service_movement(self, movement_type, stock, date, total, service_id):
        """ Insert service movement in services_movements table """

        # Parameters
        params = (round(stock, 3), movement_type, date, round(total, 2), service_id)

        # Inserte movement
        self.db.execute("INSERT INTO services_movements (units, movement_type, date, total, service_id) VALUES(?,?,?,?,?)", *params)


    def insert_product_non_identified_waste(self, date, total, product_id):
        """ Insert non identified wastes """
        
        # Parameters
        params = (round(total, 2), date, product_id)

        try:
            # Insert non indentified waste    
            self.db.execute("INSERT INTO products_non_identified_wastes (total, date, product_id) VALUES(?,?,?)", *params)
        except ValueError:
            self.db.execute("UPDATE products_non_identified_wastes SET total = total + ? WHERE date = ? AND product_id = ?", *params)


    def insert_product_identified_waste(self, date, total, motive, product_id):
        """ Insert identified waste in identified_wastes table """

        # Parameters
        params = (round(total, 2), motive, date, product_id)
    
        # Ensure product is not inserted already with same date and motive
        try:
            # Insert
            self.db.execute("INSERT INTO products_identified_wastes (total, motive, date, product_id) VALUES(?,?,?,?)", *params)
        except ValueError:
            # Update
            self.db.execute("UPDATE products_identified_wastes SET total = total + ? WHERE motive = ? AND date = ? AND product_id = ?", *params)

    def insert_service_identified_waste(self, date, total, motive, service_id):
        """ Insert identified waste in services_identified_wastes table """

        # Parameters
        params = (round(total, 2), motive, date, service_id)
    
        # Ensure product is not inserted already with same date and motive
        try:
            # Insert
            self.db.execute("INSERT INTO services_identified_wastes (total, motive, date, service_id) VALUES(?,?,?,?)", *params)
        except ValueError:
            # Update
            self.db.execute("UPDATE services_identified_wastes SET total = total + ? WHERE motive = ? AND date = ? AND service_id = ?", *params)
        
    def insert_expense(self, expense_type, expense_total, expense_year, expense_month, insert_year, insert_month, insert_day):
        """ Insert expense in expenses tables """

        # Insert expense
        self.db.execute("INSERT INTO expenses (expense_id, total, expense_year, expense_month, insert_year, insert_month, insert_day, company_id) VALUES(?,?,?,?,?,?,?,?)", expense_type, round(expense_total, 2), expense_year, expense_month, insert_year, insert_month, insert_day, self.company_id)
        
    def insert_worker(self, worker_number: str, fullname: str, adress: str, contact: str, born_date: str, section: str, role: str, workload_day: int, workload_week: int, base_salary_month: float):
        """ Insert worker in workers table """

        # Insert worker
        self.db.execute("""INSERT INTO workers (worker_number, fullname, adress, born_date, contact, section, role, workload_day, workload_week, base_salary, company_id)
                         VALUES (?,?,?,?,?,?,?,?,?,?,?)""", worker_number, fullname, adress, born_date, contact, section, role, workload_day, workload_week, base_salary_month, self.company_id)

    def insert_absence(self, worker_id: str, start_date: str, end_date: str, total: float):
        """ Insert absence in absences table """

        # Insert absence
        self.db.execute("""INSERT INTO workers_absences (worker_id, start_date, end_date, total) VALUES(?,?,?,?)""", worker_id, start_date, end_date, total)

    def insert_worker_benefit(self, date, total, worker_id):
        """ Insert benefit in benefits table """

        # Insert benefit
        self.db.execute("INSERT INTO workers_benefits (worker_id, date, total) VALUES(?,?,?)", worker_id, date, round(total, 2))

    def insert_inventory(self, inventory_number, created_date, year_created, month_created, status):
        """ Insert inventory in inventories table """

        # Params
        params = (inventory_number, created_date, year_created, month_created, status, self.company_id)

        # Insert inventory
        self.db.execute("INSERT INTO inventories (inventory_number, created_date, year_created, month_created, status, company_id) VALUES(?,?,?,?,?,?)", *params)
    
    def insert_product_in_inventories_products(self, inventory_id, product_id, real_stock, cost_price, status):
        """ Insert product in inventories_products table """
        
        # Params
        params = (inventory_id, product_id, real_stock, 0, cost_price, status)

        # Insert product
        self.db.execute("INSERT INTO inventories_products (inventory_id, product_id, real_stock, stock_counted, cost_price, status) VALUES (?,?,?,?,?,?)", *params)

    def insert_product_sale(self, product_id, date, total, units_sell):
        """ Insert product sale in products_sales table """
        
        # Ensure product has not already a sale in the same date, else update
        try:
            self.db.execute("INSERT INTO products_sales (product_id, units_sell, date, total) VALUES(?,?,?,?)", product_id, round(units_sell, 3), date, round(total, 2))
        except ValueError:
            self.db.execute("UPDATE products_sales SET total = total + ?, units_sell = units_sell + ? WHERE date = ? AND product_id = ?", round(total, 2), round(units_sell, 3), date, product_id)

    def insert_service_sale(self, service_id, date, total, units_sell):
        """ Insert service sale in services_sales table """
        
        # Ensure service has not already a sale in the same date, else update
        try:
            self.db.execute("INSERT INTO services_sales (service_id, units_sell, date, total) VALUES(?,?,?,?)", service_id, round(units_sell, 3), date, round(total, 2))
        except ValueError:
            self.db.execute("UPDATE services_sales SET total = total + ?, units_sell = units_sell + ? WHERE date = ? AND service_id = ?", round(total, 2), round(units_sell, 3), date, service_id)

    def insert_company_sale(self, date, total, units_sell):
        """ Insert company sale in company_sales table """

        params = [round(total, 2), round(units_sell, 3), date, self.company_id]

        # Ensure company has not already a sale in the same date, else update
        try:
            self.db.execute("INSERT INTO companies_sales (total, units_sell, date, company_id) VALUES(?,?,?,?)", *params)
        except ValueError:
            self.db.execute("UPDATE companies_sales SET total = total + ?, units_sell = units_sell + ? WHERE date = ? AND company_id = ?", *params)


    def insert_product_profit(self, date, total, product_id):
        """ Insert company sale in company_sales table """

        params = [round(total, 2), date, product_id]

        # Ensure company has not already a sale in the same date, else update
        try:
            self.db.execute("INSERT INTO products_profit (total, date, product_id) VALUES(?,?,?)", *params)
        except ValueError:
            self.db.execute("UPDATE products_profit SET total = total + ? WHERE date = ? AND product_id = ?", *params)

    def insert_service_profit(self, date, total, service_id):
        """ Insert company sale in company_sales table """

        params = [round(total, 2), date, service_id]

        # Ensure company has not already a sale in the same date, else update
        try:
            self.db.execute("INSERT INTO services_profit (total, date, service_id) VALUES(?,?,?)", *params)
        except ValueError:
            self.db.execute("UPDATE services_profit SET total = total + ? WHERE date = ? AND service_id = ?", *params)

    def insert_company_profit(self, date, total):
        """ Insert company sale in company_sales table """

        params = [round(total, 2), date, self.company_id]

        # Ensure company has not already a sale in the same date, else update
        try:
            self.db.execute("INSERT INTO companies_profit (total, date, company_id) VALUES(?,?,?)", *params)
        except ValueError:
            self.db.execute("UPDATE companies_profit SET total = total + ? WHERE date = ? AND company_id = ?", *params)


    def insert_product_benefit(self, product_id, date, total):
        """ Insert regularization benefit in regularization_benefits table """
        # Ensure product has not already a regularization benefit  in the same date, else update
        try:
            self.db.execute("INSERT INTO products_regularization_benefits (product_id, date, total) VALUES(?,?,?)", product_id, date, total)
        except ValueError:
            self.db.execute("UPDATE products_regularization_benefits SET total = total + ? WHERE date = ? AND product_id = ?", total, date, product_id)
           
    def insert_product_waste(self, date, total, product_id):
        """ Insert product waste in products_wastes table """

        params = (round(total, 2), date, product_id)

        try:
            self.db.execute("INSERT INTO products_wastes (total, date, product_id) VALUES(?,?,?)", *params)
        except ValueError:
            self.db.execute("UPDATE products_wastes SET total = total + ? WHERE date = ? AND product_id = ?", *params)

    def insert_company_waste(self, date, total):
        """ Insert waste or regularization benefit in companies_wastes table """

        params = (round(total, 2), date, self.company_id)

        try:
            self.db.execute("INSERT INTO companies_wastes (total, date, company_id) VALUES(?,?,?)", *params)
        except ValueError:
            self.db.execute("UPDATE companies_wastes SET total = total + ? WHERE date = ? AND company_id = ?", *params)

    def insert_personal_code(self, personal_code_hashed):
        """ Insert personal code in users table """

        self.db.execute("UPDATE users SET personal_code = ? WHERE id = ?", personal_code_hashed, self.user_id)


    def delete_all_products_from_temp_register_list(self):
        """ Delete products from temp_register_list table """

        # Delete all user products from temp_register_list table
        self.db.execute("DELETE FROM temp_register_list WHERE company_id = ?", self.company_id)

    def delete_product_from_temp_register_list(self, description):
        """ Delete product from temp_register_list table """

        # Delete product from temp_register_list table
        self.db.execute("DELETE FROM temp_register_list WHERE description = ? AND company_id = ?", description, self.company_id)

    def delete_product(self, product_id):
        """ Delete product from all products tables """

        # Delete product from products table
        self.db.execute("DELETE FROM products WHERE id = ? AND company_id = ?", product_id, self.company_id)


    def delete_service(self, service_id):
        """ Delete service from services tables """

        # Delete service from services table
        self.db.execute("DELETE FROM services WHERE id = ? AND company_id = ?", service_id, self.company_id)
 
    def delete_product_from_temp_order_list(self, product_id):
        """ Delete product from temp_order_list table """

        # Remove product from 'temp_order_list'
        self.db.execute("DELETE FROM temp_order_list WHERE product_id = ? AND company_id = ?", product_id, self.company_id)

    def delete_all_products_from_order_list(self):
        """ Delete all products from order list """

        # Delete all products
        self.db.execute("DELETE FROM temp_order_list WHERE company_id = ?", self.company_id)

    def delete_expense(self, expense_id):
        """ Delete expense from expenses table """
        
        # Delete expense
        self.db.execute("DELETE FROM expenses WHERE id = ?", expense_id)

    def delete_worker(self, worker_id):
        """ Delete worker from workers table """

        # Delete worker
        self.db.execute("DELETE FROM workers WHERE id = ?", worker_id)

    def delete_absences(self, worker_id, start_date=None):
        """ Delete absence from absence table """

        if start_date is not None:
            # Delete absence
            self.db.execute("DELETE FROM workers_absences WHERE worker_id = ? AND start_date = ?", worker_id, start_date)
        else:
            self.db.execute("DELETE FROM workers_absences WHERE worker_id = ?", worker_id)

    def delete_worker_benefits(self, benefit_id):
        """ Delete absence from absence table """

        # Delete absence
        self.db.execute("DELETE FROM workers_benefits WHERE id = ?", benefit_id)
    
    def delete_inventory(self, inventory_id):
        """ Delete inventory from inventories and inventories_products table """

        # Delete from inventories table
        self.db.execute("DELETE FROM inventories WHERE id = ?", inventory_id)

    