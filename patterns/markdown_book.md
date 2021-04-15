<ol type="1">
<li>Порождающие паттерны</li>
</ol>
<ul>
<li>Фабричный Метод (Factory Method).</li>
<li>Второй подпункт.</li>
<li>Третий подпункт.</li>
</ul>
<ol start="2" type="1">
<li>Структурные паттерны</li>
</ol>
<ul>
<li>Первый подпункт.</li>
<li>Второй подпункт.</li>
<li>Третий подпункт.</li>
</ul>
<ol start="3" type="1">
<li>Поведенческие паттерны</li>
</ol>
<ul>
<li>Первый подпункт.</li>
<li>Второй подпункт.</li>
<li>Третий подпункт.</li>
</ul>
<h1 id="фабричный-метод-factory-method.">Фабричный Метод (Factory Method).</h1>
<figure>
<img src="./generating/factory_method/factory_method.png" alt="Фабричный Метод" /><figcaption aria-hidden="true">Фабричный Метод</figcaption>
</figure>
<ol type="1">
<li>Порождающие паттерны</li>
</ol>
<ul>
<li>Фабричный Метод (Factory Method).</li>
<li>Второй подпункт.</li>
<li>Третий подпункт.</li>
</ul>
<ol start="2" type="1">
<li>Структурные паттерны</li>
</ol>
<ul>
<li>Первый подпункт.</li>
<li>Второй подпункт.</li>
<li>Третий подпункт.</li>
</ul>
<ol start="3" type="1">
<li>Поведенческие паттерны</li>
</ol>
<ul>
<li>Первый подпункт.</li>
<li>Второй подпункт.</li>
<li>Третий подпункт.</li>
</ul>
<h1 id="фабричный-метод-factory-method.-1">Фабричный Метод (Factory Method).</h1>
<figure>
<img src="./generating/factory_method/factory_method.png" alt="Фабричный Метод" /><figcaption aria-hidden="true">Фабричный Метод</figcaption>
</figure>
<ol type="1">
<li>Порождающие паттерны</li>
</ol>
<ul>
<li>Фабричный Метод (Factory Method).</li>
<li>Второй подпункт.</li>
<li>Третий подпункт.</li>
</ul>
<ol start="2" type="1">
<li>Структурные паттерны</li>
</ol>
<ul>
<li>Первый подпункт.</li>
<li>Второй подпункт.</li>
<li>Третий подпункт.</li>
</ul>
<ol start="3" type="1">
<li>Поведенческие паттерны</li>
</ol>
<ul>
<li>Первый подпункт.</li>
<li>Второй подпункт.</li>
<li>Третий подпункт.</li>
</ul>
<h1 id="фабричный-метод-factory-method.-2">Фабричный Метод (Factory Method).</h1>
<figure>
<img src="./generating/factory_method/factory_method.png" alt="Фабричный Метод" /><figcaption aria-hidden="true">Фабричный Метод</figcaption>
</figure>
<ol type="1">
<li>Порождающие паттерны</li>
</ol>
<ul>
<li>Фабричный Метод (Factory Method).</li>
<li>Второй подпункт.</li>
<li>Третий подпункт.</li>
</ul>
<ol start="2" type="1">
<li>Структурные паттерны</li>
</ol>
<ul>
<li>Первый подпункт.</li>
<li>Второй подпункт.</li>
<li>Третий подпункт.</li>
</ul>
<ol start="3" type="1">
<li>Поведенческие паттерны</li>
</ol>
<ul>
<li>Первый подпункт.</li>
<li>Второй подпункт.</li>
<li>Третий подпункт.</li>
</ul>
<h1 id="фабричный-метод-factory-method">Фабричный Метод (Factory Method)</h1>
<figure>
<img src="./generating/factory_method/factory_method.png" alt="Фабричный Метод" /><figcaption aria-hidden="true">Фабричный Метод</figcaption>
</figure>
<div class="sourceCode" id="cb1"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb1-1"><a href="#cb1-1" aria-hidden="true" tabindex="-1"></a>s <span class="op">=</span> <span class="st">&quot;Подсветка Python&quot;</span></span>
<span id="cb1-2"><a href="#cb1-2" aria-hidden="true" tabindex="-1"></a><span class="bu">print</span> s</span></code></pre></div>
<div class="sourceCode" id="cb2"><pre class="sourceCode python"><code class="sourceCode python"><span id="cb2-1"><a href="#cb2-1" aria-hidden="true" tabindex="-1"></a><span class="co">#!/usr/bin/env python</span></span>
<span id="cb2-2"><a href="#cb2-2" aria-hidden="true" tabindex="-1"></a><span class="co"># -*- coding: utf-8 -*-</span></span>
<span id="cb2-3"><a href="#cb2-3" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-4"><a href="#cb2-4" aria-hidden="true" tabindex="-1"></a><span class="co">&quot;&quot;&quot;</span></span>
<span id="cb2-5"><a href="#cb2-5" aria-hidden="true" tabindex="-1"></a><span class="co">@author: Eugene Duboviy &lt;eugene.dubovoy@gmail.com&gt; | github.com/duboviy</span></span>
<span id="cb2-6"><a href="#cb2-6" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-7"><a href="#cb2-7" aria-hidden="true" tabindex="-1"></a><span class="co">In Blackboard pattern several specialised sub-systems (knowledge sources)</span></span>
<span id="cb2-8"><a href="#cb2-8" aria-hidden="true" tabindex="-1"></a><span class="co">assemble their knowledge to build a possibly partial or approximate solution.</span></span>
<span id="cb2-9"><a href="#cb2-9" aria-hidden="true" tabindex="-1"></a><span class="co">In this way, the sub-systems work together to solve the problem,</span></span>
<span id="cb2-10"><a href="#cb2-10" aria-hidden="true" tabindex="-1"></a><span class="co">where the solution is the sum of its parts.</span></span>
<span id="cb2-11"><a href="#cb2-11" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-12"><a href="#cb2-12" aria-hidden="true" tabindex="-1"></a><span class="co">https://en.wikipedia.org/wiki/Blackboard_system</span></span>
<span id="cb2-13"><a href="#cb2-13" aria-hidden="true" tabindex="-1"></a><span class="co">&quot;&quot;&quot;</span></span>
<span id="cb2-14"><a href="#cb2-14" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-15"><a href="#cb2-15" aria-hidden="true" tabindex="-1"></a><span class="im">import</span> abc</span>
<span id="cb2-16"><a href="#cb2-16" aria-hidden="true" tabindex="-1"></a><span class="im">import</span> random</span>
<span id="cb2-17"><a href="#cb2-17" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-18"><a href="#cb2-18" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-19"><a href="#cb2-19" aria-hidden="true" tabindex="-1"></a><span class="kw">class</span> Blackboard(<span class="bu">object</span>):</span>
<span id="cb2-20"><a href="#cb2-20" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-21"><a href="#cb2-21" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> <span class="fu">__init__</span>(<span class="va">self</span>):</span>
<span id="cb2-22"><a href="#cb2-22" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.experts <span class="op">=</span> []</span>
<span id="cb2-23"><a href="#cb2-23" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.common_state <span class="op">=</span> {</span>
<span id="cb2-24"><a href="#cb2-24" aria-hidden="true" tabindex="-1"></a>            <span class="st">&#39;problems&#39;</span>: <span class="dv">0</span>,</span>
<span id="cb2-25"><a href="#cb2-25" aria-hidden="true" tabindex="-1"></a>            <span class="st">&#39;suggestions&#39;</span>: <span class="dv">0</span>,</span>
<span id="cb2-26"><a href="#cb2-26" aria-hidden="true" tabindex="-1"></a>            <span class="st">&#39;contributions&#39;</span>: [],</span>
<span id="cb2-27"><a href="#cb2-27" aria-hidden="true" tabindex="-1"></a>            <span class="st">&#39;progress&#39;</span>: <span class="dv">0</span>   <span class="co"># percentage, if 100 -&gt; task is finished</span></span>
<span id="cb2-28"><a href="#cb2-28" aria-hidden="true" tabindex="-1"></a>        }</span>
<span id="cb2-29"><a href="#cb2-29" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-30"><a href="#cb2-30" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> add_expert(<span class="va">self</span>, expert):</span>
<span id="cb2-31"><a href="#cb2-31" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.experts.append(expert)</span>
<span id="cb2-32"><a href="#cb2-32" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-33"><a href="#cb2-33" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-34"><a href="#cb2-34" aria-hidden="true" tabindex="-1"></a><span class="kw">class</span> Controller(<span class="bu">object</span>):</span>
<span id="cb2-35"><a href="#cb2-35" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-36"><a href="#cb2-36" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> <span class="fu">__init__</span>(<span class="va">self</span>, blackboard):</span>
<span id="cb2-37"><a href="#cb2-37" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard <span class="op">=</span> blackboard</span>
<span id="cb2-38"><a href="#cb2-38" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-39"><a href="#cb2-39" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> run_loop(<span class="va">self</span>):</span>
<span id="cb2-40"><a href="#cb2-40" aria-hidden="true" tabindex="-1"></a>        <span class="cf">while</span> <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;progress&#39;</span>] <span class="op">&lt;</span> <span class="dv">100</span>:</span>
<span id="cb2-41"><a href="#cb2-41" aria-hidden="true" tabindex="-1"></a>            <span class="cf">for</span> expert <span class="kw">in</span> <span class="va">self</span>.blackboard.experts:</span>
<span id="cb2-42"><a href="#cb2-42" aria-hidden="true" tabindex="-1"></a>                <span class="cf">if</span> expert.is_eager_to_contribute:</span>
<span id="cb2-43"><a href="#cb2-43" aria-hidden="true" tabindex="-1"></a>                    expert.contribute()</span>
<span id="cb2-44"><a href="#cb2-44" aria-hidden="true" tabindex="-1"></a>        <span class="cf">return</span> <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;contributions&#39;</span>]</span>
<span id="cb2-45"><a href="#cb2-45" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-46"><a href="#cb2-46" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-47"><a href="#cb2-47" aria-hidden="true" tabindex="-1"></a><span class="kw">class</span> AbstractExpert(<span class="bu">object</span>):</span>
<span id="cb2-48"><a href="#cb2-48" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-49"><a href="#cb2-49" aria-hidden="true" tabindex="-1"></a>    __metaclass__ <span class="op">=</span> abc.ABCMeta</span>
<span id="cb2-50"><a href="#cb2-50" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-51"><a href="#cb2-51" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> <span class="fu">__init__</span>(<span class="va">self</span>, blackboard):</span>
<span id="cb2-52"><a href="#cb2-52" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard <span class="op">=</span> blackboard</span>
<span id="cb2-53"><a href="#cb2-53" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-54"><a href="#cb2-54" aria-hidden="true" tabindex="-1"></a>    <span class="at">@abc.abstractproperty</span></span>
<span id="cb2-55"><a href="#cb2-55" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> is_eager_to_contribute(<span class="va">self</span>):</span>
<span id="cb2-56"><a href="#cb2-56" aria-hidden="true" tabindex="-1"></a>        <span class="cf">raise</span> <span class="pp">NotImplementedError</span>(<span class="st">&#39;Must provide implementation in subclass.&#39;</span>)</span>
<span id="cb2-57"><a href="#cb2-57" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-58"><a href="#cb2-58" aria-hidden="true" tabindex="-1"></a>    <span class="at">@abc.abstractmethod</span></span>
<span id="cb2-59"><a href="#cb2-59" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> contribute(<span class="va">self</span>):</span>
<span id="cb2-60"><a href="#cb2-60" aria-hidden="true" tabindex="-1"></a>        <span class="cf">raise</span> <span class="pp">NotImplementedError</span>(<span class="st">&#39;Must provide implementation in subclass.&#39;</span>)</span>
<span id="cb2-61"><a href="#cb2-61" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-62"><a href="#cb2-62" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-63"><a href="#cb2-63" aria-hidden="true" tabindex="-1"></a><span class="kw">class</span> Student(AbstractExpert):</span>
<span id="cb2-64"><a href="#cb2-64" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-65"><a href="#cb2-65" aria-hidden="true" tabindex="-1"></a>    <span class="at">@property</span></span>
<span id="cb2-66"><a href="#cb2-66" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> is_eager_to_contribute(<span class="va">self</span>):</span>
<span id="cb2-67"><a href="#cb2-67" aria-hidden="true" tabindex="-1"></a>        <span class="cf">return</span> <span class="va">True</span></span>
<span id="cb2-68"><a href="#cb2-68" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-69"><a href="#cb2-69" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> contribute(<span class="va">self</span>):</span>
<span id="cb2-70"><a href="#cb2-70" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;problems&#39;</span>] <span class="op">+=</span> random.randint(<span class="dv">1</span>, <span class="dv">10</span>)</span>
<span id="cb2-71"><a href="#cb2-71" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;suggestions&#39;</span>] <span class="op">+=</span> random.randint(<span class="dv">1</span>, <span class="dv">10</span>)</span>
<span id="cb2-72"><a href="#cb2-72" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;contributions&#39;</span>] <span class="op">+=</span> [<span class="va">self</span>.__class__.<span class="va">__name__</span>]</span>
<span id="cb2-73"><a href="#cb2-73" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;progress&#39;</span>] <span class="op">+=</span> random.randint(<span class="dv">1</span>, <span class="dv">2</span>)</span>
<span id="cb2-74"><a href="#cb2-74" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-75"><a href="#cb2-75" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-76"><a href="#cb2-76" aria-hidden="true" tabindex="-1"></a><span class="kw">class</span> Scientist(AbstractExpert):</span>
<span id="cb2-77"><a href="#cb2-77" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-78"><a href="#cb2-78" aria-hidden="true" tabindex="-1"></a>    <span class="at">@property</span></span>
<span id="cb2-79"><a href="#cb2-79" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> is_eager_to_contribute(<span class="va">self</span>):</span>
<span id="cb2-80"><a href="#cb2-80" aria-hidden="true" tabindex="-1"></a>        <span class="cf">return</span> random.randint(<span class="dv">0</span>, <span class="dv">1</span>)</span>
<span id="cb2-81"><a href="#cb2-81" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-82"><a href="#cb2-82" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> contribute(<span class="va">self</span>):</span>
<span id="cb2-83"><a href="#cb2-83" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;problems&#39;</span>] <span class="op">+=</span> random.randint(<span class="dv">10</span>, <span class="dv">20</span>)</span>
<span id="cb2-84"><a href="#cb2-84" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;suggestions&#39;</span>] <span class="op">+=</span> random.randint(<span class="dv">10</span>, <span class="dv">20</span>)</span>
<span id="cb2-85"><a href="#cb2-85" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;contributions&#39;</span>] <span class="op">+=</span> [<span class="va">self</span>.__class__.<span class="va">__name__</span>]</span>
<span id="cb2-86"><a href="#cb2-86" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;progress&#39;</span>] <span class="op">+=</span> random.randint(<span class="dv">10</span>, <span class="dv">30</span>)</span>
<span id="cb2-87"><a href="#cb2-87" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-88"><a href="#cb2-88" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-89"><a href="#cb2-89" aria-hidden="true" tabindex="-1"></a><span class="kw">class</span> Professor(AbstractExpert):</span>
<span id="cb2-90"><a href="#cb2-90" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-91"><a href="#cb2-91" aria-hidden="true" tabindex="-1"></a>    <span class="at">@property</span></span>
<span id="cb2-92"><a href="#cb2-92" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> is_eager_to_contribute(<span class="va">self</span>):</span>
<span id="cb2-93"><a href="#cb2-93" aria-hidden="true" tabindex="-1"></a>        <span class="cf">return</span> <span class="va">True</span> <span class="cf">if</span> <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;problems&#39;</span>] <span class="op">&gt;</span> <span class="dv">100</span> <span class="cf">else</span> <span class="va">False</span></span>
<span id="cb2-94"><a href="#cb2-94" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-95"><a href="#cb2-95" aria-hidden="true" tabindex="-1"></a>    <span class="kw">def</span> contribute(<span class="va">self</span>):</span>
<span id="cb2-96"><a href="#cb2-96" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;problems&#39;</span>] <span class="op">+=</span> random.randint(<span class="dv">1</span>, <span class="dv">2</span>)</span>
<span id="cb2-97"><a href="#cb2-97" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;suggestions&#39;</span>] <span class="op">+=</span> random.randint(<span class="dv">10</span>, <span class="dv">20</span>)</span>
<span id="cb2-98"><a href="#cb2-98" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;contributions&#39;</span>] <span class="op">+=</span> [<span class="va">self</span>.__class__.<span class="va">__name__</span>]</span>
<span id="cb2-99"><a href="#cb2-99" aria-hidden="true" tabindex="-1"></a>        <span class="va">self</span>.blackboard.common_state[<span class="st">&#39;progress&#39;</span>] <span class="op">+=</span> random.randint(<span class="dv">10</span>, <span class="dv">100</span>)</span>
<span id="cb2-100"><a href="#cb2-100" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-101"><a href="#cb2-101" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-102"><a href="#cb2-102" aria-hidden="true" tabindex="-1"></a><span class="cf">if</span> <span class="va">__name__</span> <span class="op">==</span> <span class="st">&#39;__main__&#39;</span>:</span>
<span id="cb2-103"><a href="#cb2-103" aria-hidden="true" tabindex="-1"></a>    blackboard <span class="op">=</span> Blackboard()</span>
<span id="cb2-104"><a href="#cb2-104" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-105"><a href="#cb2-105" aria-hidden="true" tabindex="-1"></a>    blackboard.add_expert(Student(blackboard))</span>
<span id="cb2-106"><a href="#cb2-106" aria-hidden="true" tabindex="-1"></a>    blackboard.add_expert(Scientist(blackboard))</span>
<span id="cb2-107"><a href="#cb2-107" aria-hidden="true" tabindex="-1"></a>    blackboard.add_expert(Professor(blackboard))</span>
<span id="cb2-108"><a href="#cb2-108" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-109"><a href="#cb2-109" aria-hidden="true" tabindex="-1"></a>    c <span class="op">=</span> Controller(blackboard)</span>
<span id="cb2-110"><a href="#cb2-110" aria-hidden="true" tabindex="-1"></a>    contributions <span class="op">=</span> c.run_loop()</span>
<span id="cb2-111"><a href="#cb2-111" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-112"><a href="#cb2-112" aria-hidden="true" tabindex="-1"></a>    <span class="im">from</span> pprint <span class="im">import</span> pprint</span>
<span id="cb2-113"><a href="#cb2-113" aria-hidden="true" tabindex="-1"></a>    pprint(contributions)</span>
<span id="cb2-114"><a href="#cb2-114" aria-hidden="true" tabindex="-1"></a></span>
<span id="cb2-115"><a href="#cb2-115" aria-hidden="true" tabindex="-1"></a><span class="co">### OUTPUT </span><span class="al">###</span></span>
<span id="cb2-116"><a href="#cb2-116" aria-hidden="true" tabindex="-1"></a><span class="co"># [&#39;Student&#39;,</span></span>
<span id="cb2-117"><a href="#cb2-117" aria-hidden="true" tabindex="-1"></a><span class="co">#  &#39;Student&#39;,</span></span>
<span id="cb2-118"><a href="#cb2-118" aria-hidden="true" tabindex="-1"></a><span class="co">#  &#39;Scientist&#39;,</span></span>
<span id="cb2-119"><a href="#cb2-119" aria-hidden="true" tabindex="-1"></a><span class="co">#  &#39;Student&#39;,</span></span>
<span id="cb2-120"><a href="#cb2-120" aria-hidden="true" tabindex="-1"></a><span class="co">#  &#39;Scientist&#39;,</span></span>
<span id="cb2-121"><a href="#cb2-121" aria-hidden="true" tabindex="-1"></a><span class="co">#  &#39;Student&#39;,</span></span>
<span id="cb2-122"><a href="#cb2-122" aria-hidden="true" tabindex="-1"></a><span class="co">#  &#39;Scientist&#39;,</span></span>
<span id="cb2-123"><a href="#cb2-123" aria-hidden="true" tabindex="-1"></a><span class="co">#  &#39;Student&#39;,</span></span>
<span id="cb2-124"><a href="#cb2-124" aria-hidden="true" tabindex="-1"></a><span class="co">#  &#39;Scientist&#39;,</span></span>
<span id="cb2-125"><a href="#cb2-125" aria-hidden="true" tabindex="-1"></a><span class="co">#  &#39;Student&#39;,</span></span>
<span id="cb2-126"><a href="#cb2-126" aria-hidden="true" tabindex="-1"></a><span class="co">#  &#39;Scientist&#39;,</span></span>
<span id="cb2-127"><a href="#cb2-127" aria-hidden="true" tabindex="-1"></a><span class="co">#  &#39;Professor&#39;]</span></span></code></pre></div>
