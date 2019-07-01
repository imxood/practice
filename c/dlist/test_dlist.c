#include "dlist.h"

int main(int argc, char const *argv[])
{
	sys_dlist_t list;

	sys_dlist_init(&list);

	sys_dnode_t node_1;
	sys_dnode_t node_2;
	sys_dnode_t node_3;
	sys_dnode_t node_4;

	sys_dlist_append(&list, &node_1);
	sys_dlist_append(&list, &node_2);
	sys_dlist_append(&list, &node_3);
	sys_dlist_append(&list, &node_4);

	sys_dnode_t *pnode;

	pnode = &list;

	printf("plist: %p\n", pnode);
	printf("\tphead: %p\n", pnode->head);
	printf("\tptail: %p\n", pnode->tail);
	printf("\tpnext: %p\n", pnode->next);
	printf("\tpprev: %p\n", pnode->prev);

	SYS_DLIST_FOR_EACH_NODE(&list, pnode) {
		printf("pnode: %p\n", pnode);
		printf("\tphead: %p\n", pnode->head);
		printf("\tptail: %p\n", pnode->tail);
		printf("\tpnext: %p\n", pnode->next);
		printf("\tpprev: %p\n", pnode->prev);
	}

	return 0;
}
