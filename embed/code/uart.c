
#include "shell.h"
#include "usart.h"
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"

#define uart USART2
#define USARTx_IRQHandler USART2_IRQHandler
static IRQn_Type irq_type = USART2_IRQn;

SHELL_TypeDef shell;

static QueueHandle_t queue;

void USARTx_IRQHandler(void)
{
	__IO uint8_t received_char;
	if (LL_USART_IsEnabledIT_RXNE(uart) && LL_USART_IsActiveFlag_RXNE(uart))
	{
		received_char = LL_USART_ReceiveData8(uart);
		xQueueSendFromISR(queue, &received_char, NULL);
	}
}

void shellTask(void *param);

static void shell_write(char data)
{
	while ((uart->ISR & 0X40) == 0)
		;
	uart->TDR = (uint16_t)(data & 0x1FFUL);
}

static signed char shell_read(char *data)
{
	xQueueReceive(queue, (void *)data, portMAX_DELAY);
	return 0;
}

void shell_init(void)
{
	queue = xQueueCreate(256, sizeof(uint8_t));

	// uart enable isr
	NVIC_SetPriority(irq_type, 5);
	NVIC_EnableIRQ(irq_type);
	LL_USART_EnableIT_RXNE(uart);

	shell.write = shell_write;
	shell.read = shell_read;
	shellInit(&shell);

	xTaskCreate(shellTask, "shell_task", 512, &shell, 5, NULL);
}
