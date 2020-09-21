# asyncio 学习笔记

## asyncio 过程分析

	Task 被包装成 Handle

		coroutine 被包装成 TaskStepMethWrapper 作为 Handle 的 callback 参数

		Handle
			self._context = context
			self._loop = loop
			self._callback = callback

		handle = events.Handle(callback, args, loop, None)



	create_future 的过程就是 获取 task 的过程

		ensure_future(coro_or_future, *, loop=None)
			if loop is None:
				loop = events.get_event_loop()
			task = loop.create_task(coro_or_future):
				task = tasks.Task(coro, loop=self, name=name)：
					call_soon:
						_call_soon:
							handle = events.Handle(callback, args, self, context)
							self._ready.append(handle)
			return task


	获取到 task 后就可以执行 future.add_done_callback, 给 task 添加回调函数, 这里就可以想起两个函数了:
		asyncio.ensure_future 和 asyncio.create_task, 返回值可以 add_done_callback 设置完成或异常时回调函数


	从 asyncio.run 传入 第一个 corintine 时, 会经过 create_future 过程, 于是 _ready 中有了第一个 future 函数,
	于是开始 run_until_complete 的运行


	_UnixSelectorEventLoop.run_until_complete
		self.run_forever


	_UnixSelectorEventLoop.run_forever
		events._set_running_loop(self)
		while True:
			self._run_once()
			if self._stopping:
				break


	_UnixSelectorEventLoop._run_once

		ntodo = len(self._ready)
			for i in range(ntodo):
				handle = self._ready.popleft()
				if handle._cancelled:
					continue
				else:
					handle._run():
						self._context.run(self._callback, *self._args)

	在这里的self._context.run中, 就会直接进入我们的 coroutin



	当某一个 handle 执行到 await 时:
		比如遇到 queue.get() 时:

			会去看 queue 是不是空的, 如果是的那么会创建新的 future, 同时等待 await future

			while self.empty():
				getter = self._loop.create_future()
				self._getters.append(getter)
				try:
					await getter


	如果遇到 gather 函数, 那么会在 _UnixSelectorEventLoop._ready 中添加多个future, 并运行下一次的 _run_once

	gather 函数本身只是个非 async 函数, 只是它生成了 _GatheringFuture 对象, 含有 children 成员
