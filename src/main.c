#include "pebble_os.h"
#include "pebble_app.h"
#include "pebble_fonts.h"
#include "http.h"

PBL_APP_INFO(HTTP_UUID,
             "Pebbit", "yesdnil5/sagnew",
             1, 0, /* App version */
             DEFAULT_MENU_ICON,
             APP_INFO_STANDARD_APP);


#define NUM_MENU_SECTIONS 1
#define NUM_FIRST_MENU_ITEMS 21

char titles[50][20];
	
Window window;
MenuLayer menu_layer;

int error = 0;

void start_http_request(){
	DictionaryIterator *out;
	HTTPResult result = http_out_get("http://hidden-meadow-9733.herokuapp.com/submissions", 155, &out);
	if(result != HTTP_OK){
		error = result;
		return;
	}
	result = http_out_send();
	if(result != HTTP_OK){
		error = result;
		return;
	}
}


void handle_http_success(int32_t request_id, int http_status, DictionaryIterator* sent, void* context){
	int i;
	for(i=0; i<20; i++){
		Tuple *tuple = dict_find(sent, 0);
		
		strcpy(titles[i], tuple->value->cstring);
	}
	error = 0;
}

void handle_http_failure(int32_t request_id, int http_status, void* context){
	int i;
	for(i=0; i<20; i++){
		strcpy(titles[i], "Failure\0");
	}
}

// A callback is dused to specify the amount of sections of menu items
// With this, you can dynamically add and remove sections
uint16_t menu_get_num_sections_callback(MenuLayer *me, void *data) {
  return NUM_MENU_SECTIONS;
}


// Each section has a number of items; we use a callback to specify this
// You can also dynamically add and remove items using this
uint16_t menu_get_num_rows_callback(MenuLayer *me, uint16_t section_index, void *data) {
	return NUM_FIRST_MENU_ITEMS;
}

// A callback is used to specify the height of the section header
int16_t menu_get_header_height_callback(MenuLayer *me, uint16_t section_index, void *data) {
  // This is a define provided in pebble_os.h that you may use for the default height
  return MENU_CELL_BASIC_HEADER_HEIGHT;
}

// Here we draw what each header is
void menu_draw_header_callback(GContext* ctx, const Layer *cell_layer, uint16_t section_index, void *data) {
	menu_cell_basic_header_draw(ctx, cell_layer, "Pebbit");
}


// This is the menu item draw callback where you specify what each item should look like
void menu_draw_row_callback(GContext* ctx, const Layer *cell_layer, MenuIndex *cell_index, void *data) {
  // Determine which section we're going to draw in
	menu_cell_basic_draw(ctx, cell_layer, titles[cell_index->row], "Subreddit by Username", NULL);  	
}


// Here we capture when a user selects a menu item
void menu_select_callback(MenuLayer *me, MenuIndex *cell_index, void *data) {

}


// This initializes the menu upon window load
void window_load(Window *me) {
  // Here we load the bitmap assets
  // resource_init_current_app must be called before all asset loading

  // Now we prepare to initialize the menu layer
  // We need the bounds to specify the menu layer's viewport size
  // In this case, it'll be the same as the window's
  GRect bounds = me->layer.bounds;

	start_http_request();
	
  // Initialize the menu layer
  menu_layer_init(&menu_layer, bounds);

  // Set all the callbacks for the menu layer
  menu_layer_set_callbacks(&menu_layer, NULL, (MenuLayerCallbacks){
    .get_num_sections = menu_get_num_sections_callback,
    .get_num_rows = menu_get_num_rows_callback,
    .get_header_height = menu_get_header_height_callback,
    .draw_header = menu_draw_header_callback,
    .draw_row = menu_draw_row_callback,
    .select_click = menu_select_callback,
  });

  // Bind the menu layer's click config provider to the window for interactivity
  menu_layer_set_click_config_onto_window(&menu_layer, me);

  // Add it to the window for display
  layer_add_child(&me->layer, menu_layer_get_layer(&menu_layer));
}


void window_unload(Window *me) {
  // Cleanup the menu icons
}


void handle_init(AppContextRef ctx) {
	window_init(&window, "Pebbit");
  window_stack_push(&window, true /* Animated */);
	

  // Setup the window handlers
  window_set_window_handlers(&window, (WindowHandlers){
    .load = window_load,
    .unload = window_unload,
  });
}


void pbl_main(void *params) {
  PebbleAppHandlers handlers = {
	  .init_handler = &handle_init,
	  .messaging_info = {
		  .buffer_sizes = {
			  .inbound = 124,
			  .outbound = 124,
		  }
	  }
  };
	HTTPCallbacks http_callbacks = {
    .failure = handle_http_failure,
    .success = handle_http_success,
  };
  http_register_callbacks(http_callbacks, NULL);
  app_event_loop(params, &handlers);
}