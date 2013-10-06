#include "pebble_os.h"
#include "pebble_app.h"
#include "pebble_fonts.h"


#define MY_UUID { 0x65, 0x89, 0x15, 0x18, 0xB1, 0x8E, 0x4F, 0x60, 0x85, 0x02, 0x69, 0x13, 0x89, 0x16, 0xDB, 0x9F }
PBL_APP_INFO(MY_UUID,
             "Pebbit", "LindseyCrocker/Sagnew",
             1, 0, /* App version */
             DEFAULT_MENU_ICON,
             APP_INFO_STANDARD_APP);

Window window;
TextLayer hello_layer;
SimpleMenuLayer simple_menu_layer;
SimpleMenuSection menu_sections[2];
SimpleMenuItem first_menu_items[3];
SimpleMenuItem second_menu_items[1];

void menu_select_callback(int index, void *ctx) {
	first_menu_items[index].subtitle = "You've selected here!";
	layer_mark_dirty(simple_menu_layer_get_layer(&simple_menu_layer));
}

void window_load(Window *me){
	int num_a_items = 0;
	first_menu_items[num_a_items++] = (SimpleMenuItem){
		.title = "First Item",
		.callback = menu_select_callback,
	};
	first_menu_items[num_a_items++] = (SimpleMenuItem){
		.title = "Second Item",
		.subtitle = "Here's a subtitle",
		.callback = menu_select_callback,
	};
	first_menu_items[num_a_items++] = (SimpleMenuItem){
		.title = "Third Item",
		.callback = menu_select_callback,
	};
	
	second_menu_items[0] = (SimpleMenuItem){
		.title = "Special Item, except for not",
		.callback = menu_select_callback,
	};
	
	menu_sections[0] = (SimpleMenuSection){
    	.num_items = 3,
    	.items = first_menu_items,
	};
  	menu_sections[1] = (SimpleMenuSection){
    	// Menu sections can also have titles as well
    	.title = "Yet Another Section",
    	.num_items = 1,
    	.items = second_menu_items,
 	};
	
	GRect bounds = me->layer.bounds;
	simple_menu_layer_init(&simple_menu_layer, bounds, me, menu_sections, 2, NULL);
	layer_add_child(&me->layer, simple_menu_layer_get_layer(&simple_menu_layer));

}

void handle_init(AppContextRef ctx) {
	resource_init_current_app(&APP_RESOURCES);

  	window_init(&window, "Pebbit");
  	window_stack_push(&window, true /* Animated */);
	window_set_window_handlers(&window, (WindowHandlers){
		.load = window_load,
	});
}


void pbl_main(void *params) {
  PebbleAppHandlers handlers = {
    .init_handler = &handle_init
  };
  app_event_loop(params, &handlers);
}
