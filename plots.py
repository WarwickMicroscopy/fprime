#%%
from time import process_time, perf_counter
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad_vec
from scipy.constants import pi, c, h, e, m_e
from scipy.optimize import curve_fit
from scipy.interpolate import RegularGridInterpolator

Z = 31
lobato_array = np.array([[6.473848488352918e-03,-4.901925767802290e-01,5.732841603908765e-01,-3.794033014839905e-01,5.544264747740791e-01,2.785198853791489e+00,2.776204283306448e+00,2.775385910506251e+00,2.767593028672588e+00,2.765118976429275e+00],
[3.057451160998355e+00,-6.200447791273253e+01,6.400555370846145e+01,-5.001325785427806e+00,1.517988287005264e-01,1.089672487260788e+00,9.398387981431211e-01,9.252890343862655e-01,8.229474987086506e-01,5.773931106754022e-01],
[3.926222728861479e+00,-4.548619626399980e+00,2.193353128786585e+00,6.994512650339657e-02,2.098642248519376e-03,8.142760135172804e+00,4.989410770078558e+00,4.144289992394109e+00,4.019223150656802e-01,1.564790347198236e-01],
[3.398249705570541e+00,-1.908668860956967e+00,3.907021175392274e-02,-1.116310102107145e-02,9.462044653575231e-03,4.442701786224095e+00,3.324515425264230e+00,1.897728803482149e-01,8.719186146446036e-02,8.278090600413406e-02],
[1.472792486393293e+00,-4.019330421993871e-01,3.059989569826894e-01,1.961442171731680e-02,9.771771060882025e-04,3.749740482818191e+00,5.880665361396738e-01,5.156396131030110e-01,1.213775700806037e-01,6.809824121603139e-02],
[1.244660886213433e+02,-2.203528570789638e+02,1.952353522804791e+02,-9.810793612697997e+01,1.420230412136232e-02,2.421208492560056e+00,2.305379437524258e+00,2.048519321065642e+00,1.933525529175474e+00,7.689768184783397e-02],
[5.813271507025561e+01,-1.475424090878127e+02,1.301430656496395e+02,-3.961956740841543e+01,1.059577633314809e-02,1.700448564134711e+00,1.559038526017404e+00,1.415768274731469e+00,1.278418182054558e+00,5.655877984748055e-02],
[2.994740452423624e+01,-7.761012662552783e+01,9.988177646231442e+01,-5.121270055056731e+01,8.196189544460320e-03,1.302839878800107e+00,1.157941052583095e+00,1.009885493380251e+00,9.433279714332660e-01,4.331976113218256e-02],
[9.489848945035248e-01,-3.013339230435549e+01,5.279650781273386e+01,-2.270627037952724e+01,6.569976645314410e-03,1.458829331986459e+00,6.887799931876800e-01,6.542398693466957e-01,6.148361308119943e-01,3.428374194950112e-02],
[5.827411922209074e-01,3.706765618410549e-01,-5.467449673508092e-01,4.140526824802081e-01,5.199030808639931e-03,1.281185731438772e+00,4.445208971704776e-01,1.986508755104810e-01,1.854772466562765e-01,2.757383820338858e-02],
[2.367006039467926e+01,-2.185317861597425e+01,5.924994481089464e-01,-2.446522903102440e-02,4.839502217065358e-03,8.451487735146031e+00,8.040966004742982e+00,6.249960005263150e-01,1.324503949472964e-01,2.339943620498786e-02],
[4.855010476871495e+00,-2.662209064768437e+00,4.780012360851080e-01,-7.023070646920648e-02,3.989058281040198e-03,5.946392738424565e+00,4.171303125206979e+00,3.982698081503743e-01,1.618861858374742e-01,1.953450563631035e-02],
[2.834095616075075e+00,-4.280041333782610e+00,4.421916805483114e+00,-3.457744718964006e-02,3.523859414060799e-03,6.662350239805332e+00,5.512947222240214e-01,5.093289634459738e-01,1.117848374253312e-01,1.676023518052574e-02],
[2.871891426116124e+00,-2.061735011951735e+00,2.171140242044787e+00,-6.630736330588019e-02,3.010707096705137e-03,5.084871036429896e+00,4.291781853051262e-01,3.664854341921622e-01,1.197106112969034e-01,1.439945361283975e-02],
[2.791518400231514e+00,-4.365068378238221e+00,4.435584555166990e+00,-8.096357733994739e-02,2.679000179664404e-03,3.900659618654661e+00,3.298259683771500e-01,3.060899565058886e-01,1.080832325459728e-01,1.258944953311868e-02],
[2.679714156101995e+00,-4.742528222307552e-01,5.148359489896877e-01,-9.583600249907225e-02,2.488719638189352e-03,3.068891211999711e+00,3.782167021858090e-01,1.887218119025488e-01,9.233705900314941e-02,1.119208772411441e-02],
[2.566248399800203e+00,-3.388763508285917e-01,1.145845587555150e+00,-9.231093165470796e-01,2.291680020410422e-03,2.415949203656124e+00,4.214142393102160e-01,1.095924049758303e-01,9.909554582267530e-02,9.996659489275210e-03],
[2.459817464140685e+00,-3.641981770769951e-01,2.505844772224745e-01,-5.774370295443458e-02,2.301438668285837e-03,1.940046319888566e+00,3.992410678843988e-01,1.174724062744122e-01,5.678037260236218e-02,9.155798329207080e-03],
[5.811078786014548e+00,-5.025370965394226e+01,4.886094120598425e+01,7.406285920483829e-02,7.278027386262219e-04,1.266914833990368e+01,3.956410396981665e+00,3.683850595771545e+00,1.074585175695628e-01,6.655767893915011e-03],
[2.117811615241595e+01,-3.390438243174689e+02,3.227569585232967e+02,6.500776738969967e-02,6.558743665785935e-04,6.396086194317362e+00,3.740247138917495e+00,3.648884499226053e+00,9.450906345146735e-02,5.985206198837586e-03],
[1.260351865721486e+01,-2.768753820537026e+02,2.688716039073428e+02,5.568241788974580e-02,5.770712551453996e-04,6.156256153638529e+00,3.088735542666793e+00,3.027276632985483e+00,8.188747483752157e-02,5.382898320507976e-03],
[8.575957752381299e+00,-2.103315634653049e+02,2.060971726015414e+02,4.777739489772619e-02,5.057164844803206e-04,6.007806688755818e+00,2.602858567452130e+00,2.553523450511056e+00,7.114294840241539e-02,4.856284393837261e-03],
[6.527684332347890e+00,-2.004305768291727e+02,1.980150538899940e+02,4.139115180640056e-02,4.474550243298565e-04,5.835524793524481e+00,2.232559523811276e+00,2.197860185942290e+00,6.239738768285473e-02,4.403836490799580e-03],
[3.028317848436913e+00,-9.553939330814323e+01,9.617615623521981e+01,3.597773159579877e-02,3.914928907184223e-04,8.359115043146318e+00,1.802637902641032e+00,1.775094889570472e+00,5.481444121431137e-02,3.998289689160348e-03],
[4.374175506331227e+00,-1.609255109187795e+02,1.602733080603223e+02,3.123038610491624e-02,3.469660210209380e-04,5.510317055049282e+00,1.687982164024339e+00,1.666140477777024e+00,4.833703903212770e-02,3.647469600530682e-03],
[3.798100908368596e+00,-9.168935493816872e+01,9.144542521554298e+01,2.727543440276047e-02,3.033798543837710e-04,5.317126458994331e+00,1.497130948847481e+00,1.468092418044105e+00,4.272478501289549e-02,3.327918552318741e-03],
[3.330378744675443e+00,-7.700175964729671e+01,7.707252217905169e+01,2.399046690405699e-02,2.682566655239420e-04,5.181359645795432e+00,1.329151222651394e+00,1.302849289632289e+00,3.806454868263710e-02,3.050100079915708e-03],
[2.969080787252864e+00,-7.574770691290402e+01,7.603982876253073e+01,2.101621136929670e-02,2.311517511351530e-04,5.041809491093800e+00,1.182755079216293e+00,1.162165458466299e+00,3.374790878830353e-02,2.786808620707405e-03],
[1.752071452121456e+00,-4.304105234921245e+01,4.407059155435739e+01,1.868761540881447e-02,2.017273247916241e-04,6.187504979861871e+00,1.002662636289766e+00,9.853843113530303e-01,3.029847039161176e-02,2.558555987488791e-03],
[2.466371104994591e+00,-6.146785413325375e+01,6.201769452374813e+01,1.641601739314162e-02,1.724871175953809e-04,4.910280784938159e+00,9.678985203229922e-01,9.512838347753555e-01,2.696009676675663e-02,2.341096110462537e-03],
[2.760102031084283e+00,-3.444526142074679e+01,3.522622672440163e+01,1.320671969994199e-02,1.259455609282457e-04,6.101282245376627e+00,7.651433135534649e-01,7.513286233828597e-01,2.248796343172512e-02,2.067373742787123e-03],
[3.182416352600000e+00,-5.245140378111667e+01,5.296908271622185e+01,1.140961685918648e-02,9.509543581450579e-05,5.017190408609147e+00,7.123957644377982e-01,7.022801925281940e-01,1.967472956940154e-02,1.841466144940115e-03],
[3.456429691196040e+00,-3.331760444317212e+01,3.357121938553322e+01,9.790022956403421e-03,6.534348622651725e-05,4.013580160329452e+00,6.623557780506291e-01,6.457719410560738e-01,1.709193532310115e-02,1.603016028394201e-03],
[3.649050478019264e+00,-4.368516622212386e+01,4.369202886011548e+01,8.449022841991444e-03,3.786114741100382e-05,3.250432671125934e+00,6.096662016502890e-01,5.969713008021232e-01,1.485545127403623e-02,1.336255873565630e-03],
[3.838463122242895e+00,-5.227234710112339e+01,5.198612794956596e+01,7.339559893380448e-03,1.646942079513399e-05,2.611894705732323e+00,5.661950628747182e-01,5.552793266998739e-01,1.297464694324407e-02,1.029865368558757e-03],
[4.025410303108274e+00,-4.630423320789298e+01,4.572136819041012e+01,6.353379596253157e-03,1.334778452557430e-06,2.136483814437400e+00,5.265911664541312e-01,5.141367844645776e-01,1.128072422420068e-02,4.880898579409704e-04],
[3.389753515953940e+00,2.143483486791724e+00,3.543226035109782e-01,3.740093400856642e-03,3.003425023422297e-07,2.057448143681711e+01,1.910799452185164e+00,1.974105893966039e-01,8.134594653439889e-03,2.926857910569511e-04],
[4.770925092998260e+00,1.475978501552834e+00,3.044513555441887e-01,3.594749819167283e-03,3.000855492282790e-07,1.336688813304128e+01,1.337383795771967e+00,1.775323694377828e-01,7.791050330018268e-03,2.822551396485372e-04],
[4.607210198752340e+00,1.428018510398403e+00,2.955810455777538e-01,3.389978408528951e-03,2.668629749690224e-07,1.086869055571519e+01,1.311374558731241e+00,1.680228707847112e-01,7.359645453504783e-03,2.623432810213873e-04],
[4.311754534068716e+00,1.493315780393395e+00,2.812360501288841e-01,3.093377384557471e-03,2.580244485125306e-07,9.458965805174902e+00,1.330636228452456e+00,1.565068714444536e-01,6.824105238117352e-03,2.498188791107023e-04],
[3.111790391134954e+00,2.202590609458031e+00,2.703307749100209e-01,2.687991947510981e-03,2.325494833477792e-07,1.069031413430237e+01,1.653163561589331e+00,1.451151857189699e-01,6.139563515828505e-03,2.322402359376725e-04],
[2.831059684320536e+00,2.348581374896745e+00,2.451058884296964e-01,2.352821082185159e-03,2.312708383438592e-07,1.043571957589507e+01,1.604828686745972e+00,1.316969347746069e-01,5.549779013833459e-03,2.227474637648977e-04],
[2.571798593233526e+00,2.456337419572030e+00,2.206584408813715e-01,2.055314180124382e-03,2.321329477936922e-07,1.016431171313775e+01,1.534419192445505e+00,1.191386197541104e-01,5.018532408829888e-03,2.145903791208612e-04],
[2.332300303539466e+00,2.535780254890496e+00,1.982080421360260e-01,1.761201304600535e-03,1.981294115460245e-07,9.921674601599595e+00,1.455856688087881e+00,1.076821878733493e-01,4.472435456549673e-03,1.965747162324994e-04],
[2.113525348594700e+00,2.586363161550138e+00,1.770639138636865e-01,1.497370510030569e-03,2.054814455556224e-07,9.659137258597623e+00,1.371066569343296e+00,9.703530275846488e-02,3.971285090887921e-03,1.913551907377983e-04],
[6.421597961826873e-01,2.979148144263289e+00,1.681544260042708e-01,1.337442138784078e-03,1.914109682468616e-07,5.974797502634061e+00,1.433594325412777e+00,9.098684011726770e-02,3.624101371161622e-03,1.806889144160450e-04],
[1.553172166803896e+00,2.639303646999888e+00,1.420154869567882e-01,1.008504600997609e-03,1.946384299730244e-07,8.156202357589566e+00,1.216008874818015e+00,7.900988649158734e-02,2.965479013639490e-03,1.745930959191462e-04],
[6.153078519928602e+01,-7.860167412015821e+01,2.155012926027705e+01,1.376850156641916e-01,3.246449309465210e-04,3.114681025332473e+00,2.760169833885745e+00,1.935513123247224e+00,7.224683472602932e-02,1.170016296246845e-03],
[4.222321779015246e+00,-2.641213183532026e+01,2.728528527087469e+01,1.216179018841380e-01,3.068835463715258e-04,6.072655104032275e+00,1.645501789593879e+00,1.522570749395068e+00,6.565079146952256e-02,1.120938514730356e-03],
[5.142220746420537e+00,-2.549454137625767e+01,2.574144875486019e+01,1.117782275921996e-01,2.936473847377427e-04,5.272726364744845e+00,1.531949592091483e+00,1.402575250400872e+00,6.116853872630869e-02,1.075608153945223e-03],
[6.241640318318837e+00,-9.338687244195522e+01,9.263328758298843e+01,1.034126922212987e-01,2.818484268943907e-04,4.269841080826875e+00,1.394077461402502e+00,1.355668549104345e+00,5.726679496521998e-02,1.033079542820674e-03],
[7.377433018134030e+00,-1.260251069316281e+02,1.241284050040956e+02,9.599783718185698e-02,2.710722163988820e-04,3.469177577838978e+00,1.297598108867366e+00,1.267710676460660e+00,5.377717501794231e-02,9.930845770291768e-04],
[9.644006662721232e+00,-1.229244353501125e+02,1.186825648165673e+02,8.950259470255390e-02,2.612761214904750e-04,2.726455453665441e+00,1.237234258508660e+00,1.200620368722498e+00,5.066786822851999e-02,9.554378833834973e-04],
[1.554517496748606e+01,-1.182410278567446e+02,1.080095249631970e+02,8.362593419922217e-02,2.519918624290739e-04,2.106373408654927e+00,1.208603761295122e+00,1.153952705672140e+00,4.781893912748243e-02,9.198862575926131e-04],
[4.287087391816923e+00,3.232506654229650e+00,6.740295335617063e-01,6.189080833876976e-02,2.356120529521900e-04,2.265878707985415e+01,2.237973864700642e+00,3.689955686643163e-01,4.022665752984844e-02,8.837618908780351e-04],
[6.244751873904615e+00,2.351722714163885e+00,4.742793732222520e-01,6.381138742868499e-02,2.346512805627924e-04,1.514313541909856e+01,1.453790006048140e+00,3.208356463878018e-01,4.043545320946998e-02,8.540811312800327e-04],
[6.097881795995097e+00,2.194951647366750e+00,5.481727919600226e-01,6.166695732226626e-02,2.268073558647142e-04,1.242885443158548e+01,1.505359923520235e+00,3.337380397171243e-01,3.877445534999988e-02,8.240498840648670e-04],
[5.795268796472405e+00,2.370226641078433e+00,4.713987569011149e-01,5.743682605878668e-02,2.189794892596593e-04,1.428010550582560e+01,1.359690157191345e+00,3.020173496635141e-01,3.664367981470077e-02,7.954345265183711e-04],
[5.604062553775258e+00,2.357962595618129e+00,4.760010985728824e-01,5.441233743152471e-02,2.114146022051498e-04,1.395174902305747e+01,1.312397549174392e+00,2.949337011929565e-01,3.486015424623241e-02,7.682616826618097e-04],
[5.429083919697703e+00,2.336873253608803e+00,4.833735541048819e-01,5.146549645574790e-02,2.037761328637611e-04,1.365036494276600e+01,1.267598413903199e+00,2.886106815769299e-01,3.312918074466093e-02,7.423484838012663e-04],
[5.267744450894446e+00,2.308558133263050e+00,4.932654790260128e-01,4.863562797416966e-02,1.963088423206752e-04,1.336020968273946e+01,1.225858565869417e+00,2.829196321278669e-01,3.147353971271379e-02,7.176580250696152e-04],
[5.126804285170776e+00,2.269255340083806e+00,5.042093004533025e-01,4.569239924162220e-02,1.886750504938862e-04,1.315815010261290e+01,1.181295082433371e+00,2.771070382190629e-01,2.979576045495446e-02,6.940110991990983e-04],
[4.979623597498092e+00,2.241830874556695e+00,5.129339614028937e-01,4.298018484983344e-02,1.813816924857876e-04,1.283926630780338e+01,1.147054464204860e+00,2.703871609352437e-01,2.824187149526020e-02,6.714866031739924e-04],
[5.078358300456114e+00,1.957440271816590e+00,5.928259832213751e-01,4.195020341439256e-02,1.752410915283168e-04,1.051327254690473e+01,1.117649412815246e+00,2.843867418336752e-01,2.726633276413471e-02,6.503108607073037e-04],
[4.711616366573001e+00,2.172619507865789e+00,5.397176013428657e-01,3.797960045478111e-02,1.669237635648417e-04,1.231094159485391e+01,1.087437967674925e+00,2.598049655092755e-01,2.532899238951897e-02,6.292785669619112e-04],
[4.590755044851466e+00,2.135723730365674e+00,5.513555600941525e-01,3.560584067185138e-02,1.598240168567898e-04,1.206567406233699e+01,1.058117371158644e+00,2.539944389186618e-01,2.395087396496492e-02,6.094827484332881e-04],
[4.484001106267108e+00,2.089043470785398e+00,5.659326183161046e-01,3.327035902110630e-02,1.524456102828921e-04,1.187492506915706e+01,1.028284937087896e+00,2.489078079080760e-01,2.258440655321478e-02,5.903744451594245e-04],
[4.376651407869632e+00,2.046451503836341e+00,5.806628605915877e-01,3.123885283277667e-02,1.453748696625357e-04,1.166530807171395e+01,1.003147696754953e+00,2.441532926863124e-01,2.136185800007310e-02,5.721103384547666e-04],
[4.283083182474195e+00,1.995380014537307e+00,5.970535713325043e-01,2.909516688695599e-02,1.380647690375216e-04,1.149619059566834e+01,9.770391020188206e-01,2.394291329758291e-01,2.009122333272558e-02,5.543771384922663e-04],
[4.195638407371233e+00,1.943332859786456e+00,6.124466172854658e-01,2.715152076949324e-02,1.305947873519297e-04,1.141077504566523e+01,9.490119244548774e-01,2.349503265353047e-01,1.890515762809755e-02,5.372336492097111e-04],
[4.356925932963843e+00,1.695892047773159e+00,6.639045200684705e-01,2.630200187602814e-02,1.254973184998238e-04,9.294345147185689e+00,9.105000459574200e-01,2.387465959113764e-01,1.820985425464623e-02,5.215593719635622e-04],
[4.331384056649235e+00,1.527648647286807e+00,7.357959228912380e-01,2.495263232014026e-02,1.187408525810578e-04,7.876844338102884e+00,9.425156426277488e-01,2.416994800398060e-01,1.728998944485090e-02,5.058346313135256e-04],
[4.197260013196420e+00,1.468548067747088e+00,7.839312482110882e-01,2.324940948643951e-02,1.112613586072860e-04,6.936740248944572e+00,1.017252766183483e+00,2.389489397150706e-01,1.623324330753810e-02,4.902390040211490e-04],
[3.976297158190774e+00,1.522926842573418e+00,7.977062463905613e-01,2.136667415586852e-02,1.030786893857173e-04,6.296857792287749e+00,1.112899511576911e+00,2.310570406784734e-01,1.510135455672045e-02,4.746824771050258e-04],
[3.751443814398119e+00,1.627688029776327e+00,7.817567554542718e-01,1.951708039122916e-02,9.431998042934275e-05,5.797546360829538e+00,1.182236310777107e+00,2.199135860247702e-01,1.398104554814566e-02,4.591271258298386e-04],
[3.484015173387116e+00,1.793779204169655e+00,7.448783566919203e-01,1.754277851624345e-02,8.448723515688600e-05,5.439988460809537e+00,1.227921341401281e+00,2.062088569929092e-01,1.278994017211460e-02,4.430322267874786e-04],
[1.599565781988442e+00,2.975344521941205e+00,6.950926783668822e-01,1.487796274586880e-02,6.905495791015833e-05,5.792444473855675e+00,1.553009829732260e+00,1.886263359366482e-01,1.117634706624533e-02,4.227723616555514e-04],
[2.040215639757283e+00,2.899226346248255e+00,6.363440838157977e-01,1.320719195954083e-02,5.673821925001312e-05,6.658194296096275e+00,1.413379237789324e+00,1.740001045021790e-01,1.006878045302105e-02,4.030771056922231e-04],
[1.675934670648708e+00,3.004866029697293e+00,5.953400131616355e-01,1.171631866230948e-02,4.296782976398171e-05,5.522310932114025e+00,1.380072230071963e+00,1.622292376559454e-01,9.018148904165756e-03,3.792776674776671e-04],
[2.235228504431053e+00,2.682766386519949e+00,5.551949262124333e-01,1.072733543662587e-02,3.284739920462629e-05,5.020309889602403e+00,1.230775905837777e+00,1.522481229928636e-01,8.283991169062104e-03,3.562419389317589e-04],
[2.803427374125100e+00,2.718827879660200e+00,5.224759153919996e-01,9.845378369710420e-03,2.345245265083162e-05,6.558768728045342e+00,1.169724225166679e+00,1.435566918001781e-01,7.619765262300398e-03,3.296276739029854e-04],
[3.608610209977714e+00,2.450567747371983e+00,4.786395001072570e-01,8.872142351692152e-03,1.040019329094673e-05,6.581625946219628e+00,1.027728526605885e+00,1.335336806347209e-01,6.848612389484298e-03,2.763888754566660e-04],
[4.242099010573159e+00,2.099943420558279e+00,4.328366313799229e-01,8.020215703810592e-03,7.217850308513403e-07,5.752801155360800e+00,8.739014891954615e-01,1.235999561805247e-01,6.176003330585702e-03,1.414951776172309e-04],
[4.636200956689623e+00,1.780633114269871e+00,4.037304439527385e-01,7.685395546686740e-03,8.954159028076436e-08,4.888252997809829e+00,7.563105268800747e-01,1.173023644522492e-01,5.930343942428942e-03,7.666686638730287e-05],
[4.965922505950705e+00,1.438155615070337e+00,3.712992005792981e-01,7.472564284502011e-03,1.141152841525851e-07,4.091293787874963e+00,6.292289966025513e-01,1.110966786955352e-01,5.772350103477618e-03,8.085118938793825e-05],
[5.306156144750332e+00,1.117331602360721e+00,3.158587231108543e-01,7.203422423102100e-03,1.073553305458635e-07,3.488007354816557e+00,4.811907411497712e-01,1.018744679457531e-01,5.592453744170787e-03,7.795066735407367e-05],
[4.520533990423360e+00,4.106953979091246e+00,7.139468785037285e-01,1.692940276874539e-02,8.574921291917244e-05,1.944822342329488e+01,1.898246731559969e+00,1.695535635953418e-01,1.148195675489342e-02,3.461220382579827e-04],
[6.524010720018733e+00,3.207870807456613e+00,5.404787743496377e-01,8.782788068988532e-03,6.910106029491315e-06,1.400925542989749e+01,1.326350359616653e+00,1.314085683860361e-01,6.286474345204096e-03,2.278399814589510e-04],
[6.896028535596191e+00,2.835141545365232e+00,5.035068818888151e-01,8.022945109667069e-03,9.204009547587397e-08,1.107638256703987e+01,1.171326162905030e+00,1.234946513917999e-01,5.735155957904971e-03,7.197075418025232e-05],
[7.093749001626302e+00,2.529123739031940e+00,4.821078198888890e-01,7.719366741451110e-03,7.271141994250414e-08,9.094737951659447e+00,1.063916670331612e+00,1.186194466218779e-01,5.539457088950347e-03,6.584947305284627e-05],
[6.434013247972842e+00,2.970999705357888e+00,4.607966517878480e-01,7.240331257754553e-03,6.362366643091279e-08,1.025968513072979e+01,1.131774523061633e+00,1.127759353623823e-01,5.274595833531321e-03,6.192638240887597e-05],
[6.210708267840199e+00,3.039344538256235e+00,4.373399844391628e-01,6.807147641473166e-03,6.182293277428513e-08,1.002141058591628e+01,1.103998801558834e+00,1.072189731624539e-01,5.024321308506824e-03,6.005069941971958e-05],
[6.004315983089865e+00,3.094316545314180e+00,4.128084877164170e-01,6.408916578800669e-03,6.730073762160754e-08,9.817930467191061e+00,1.069787050680294e+00,1.016352914486458e-01,4.795248468887250e-03,6.028065987264629e-05],
[5.200617168103042e+00,3.498494403671440e+00,4.054149311313203e-01,6.223437008265299e-03,6.008593295434409e-08,1.120383101944067e+01,1.128463695469282e+00,9.893334726861316e-02,4.659174319779507e-03,5.725906389623341e-05],
[5.025338600360291e+00,3.518439882851541e+00,3.819503494462722e-01,5.821102080962110e-03,6.526093388297119e-08,1.097721906976287e+01,1.084772148326308e+00,9.367468748538359e-02,4.426823468734856e-03,5.738568370505115e-05],
[5.346561002606197e+00,3.224684665609108e+00,3.494617526254452e-01,5.292517567488151e-03,6.159176302362374e-08,9.231183797524494e+00,9.728362291938352e-01,8.705962209665623e-02,4.130119644650323e-03,5.494638944496757e-05],
[5.225823503340047e+00,3.228188739952953e+00,3.270988788238514e-01,4.888825755922390e-03,5.212722694193633e-08,9.071357066187183e+00,9.311242774566348e-01,8.207206020598455e-02,3.890296559934166e-03,5.103679766366416e-05],
[4.586412477535479e+00,3.518695956651012e+00,3.192617142012054e-01,4.729796479856258e-03,5.513244808062041e-08,1.031861020923352e+01,9.572788378292328e-01,7.968074314438807e-02,3.771931999968489e-03,5.097508603760111e-05],
[4.457994806754126e+00,3.508672126376623e+00,3.013753805283154e-01,4.407637462144819e-03,4.887879032285916e-08,1.008906933834013e+01,9.194464473616226e-01,7.564191777863293e-02,3.570264651248093e-03,4.804951743958113e-05],
[4.338975764011709e+00,3.491850988964034e+00,2.814710990162868e-01,4.002092714990461e-03,5.529298081955140e-08,9.963309372238362e+00,8.780839569829744e-01,7.116371157687776e-02,3.321524042150777e-03,4.851031794603728e-05],
[4.227294704031012e+00,3.472492275106616e+00,2.648222294968986e-01,3.690728778331929e-03,6.258714262002473e-08,9.724006020400314e+00,8.428737759602104e-01,6.735347439748511e-02,3.123646062633208e-03,4.912170970176192e-05],
[4.109517024430204e+00,3.457991325227507e+00,2.470873512223867e-01,3.304239209409952e-03,5.991049262319316e-08,9.677359945101202e+00,8.069400424708172e-01,6.328154369541671e-02,2.875446396412092e-03,4.706791536975981e-05]])

preFactor = 1e10*2*h/(m_e*c)

def lobato(s, Z):
    ab = lobato_array[Z-1]
    g = 2*s    
    f = ab[0]*(2 + ab[5]*g**2)/(1 + ab[5]*g**2)**2 + \
        ab[1]*(2 + ab[6]*g**2)/(1 + ab[6]*g**2)**2 + \
        ab[2]*(2 + ab[7]*g**2)/(1 + ab[7]*g**2)**2 + \
        ab[3]*(2 + ab[8]*g**2)/(1 + ab[8]*g**2)**2 + \
        ab[4]*(2 + ab[9]*g**2)/(1 + ab[9]*g**2)**2
    return f

def integrand(sx, sy, s, M, Z):
    s1 = np.sqrt((s/2 + sx)**2 + sy**2)
    s2 = np.sqrt((s/2 - sx)**2 + sy**2)
    s_square = sx**2 + sy**2 - (s**2/4)
    result = lobato(s1, Z)*lobato(s2, Z)*(1 - np.exp(-2*M*s_square))
    return result

def integral1(sy, s, M, Z):
    return quad_vec(integrand, 0, np.inf, args=(sy, s, M, Z))[0]

# quad_vec is used instead of something like dblquad so that 2d arrays of s and M may be calculated efficiently
def fprime(s, M, Z):
    return preFactor*4*quad_vec(integral1, 0, np.inf, args=(s, M, Z))[0]


s = 0
M = 0.7

r = np.linspace(0, 2, 200)
p = np.linspace(70*pi/180 + 0.698, 70*pi/180 - 0.698 + 2*pi, 200)
R, P = np.meshgrid(r, p)
X, Y = R*np.cos(P), R*np.sin(P)
fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize= (20,20))

#ax.set_proj_type('ortho')
z = integrand(X, Y, s, M, Z)
ax.plot_surface(X, Y, z, alpha=1)

#ax.plot_wireframe(X, Y, z, color = 'k', linewidth=0.5)
ax.view_init(elev=20, azim=70)
ax.set_xlim([-2.2, 2.2])
ax.set_ylim([-2.2, 2.2])
ax.set_zlim([0, 0.7])
ax.tick_params(axis='x', which='major', labelsize=15, pad=10)
ax.tick_params(axis='y', which='major', labelsize=15, pad=10)
ax.tick_params(axis='z', which='major', labelsize=15, pad=10)
ax.dist = 9

#%%
svals = np.linspace(0, 4, 100)
Bvals = np.linspace(0, 2, 100)
X, Y = np.meshgrid(svals, Bvals)
f = fprime(X, Y, Z)


#%%
xticks = np.arange(0, 4.5, 0.5)
yticks = np.arange(0, 2.25, 0.25)
zticks = np.arange(-350, 50, 50)


fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize= (10, 10), layout="constrained")
ax.dist = 13
ax.plot_wireframe(X, Y, f, alpha=1, linewidth=0.5)
ax.set_xlabel("s (Å⁻¹)", fontsize=12, labelpad=12)
ax.set_ylabel("B (Å²)", fontsize=12, labelpad=12)
ax.set_zlabel("f' (Å)", fontsize=12, labelpad=12)
ax.set_zscale("log")
ax.tick_params(axis='z', which='major', pad=5)

# %%
f = np.where(f>0, f, 0)

xticks = np.arange(0, 4.5, 0.5)
yticks = np.arange(0, 2.25, 0.25)
zticks = np.arange(0, 0.018, 0.002)


fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize= (10, 10), layout="tight")
ax.dist = 13
ax.plot_wireframe(X, Y, f, alpha=1, linewidth=0.5)
ax.set_xlabel("s (Å⁻¹)", fontsize=12, labelpad=12)
ax.set_ylabel("B (Å²)", fontsize=12, labelpad=12)
ax.set_zlabel("f' (Å)", fontsize=12, labelpad=18)
ax.tick_params(axis='z', which='major', pad=8)

# %%
#0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 2.75, 4
Mvals = [0.1, 0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.5, 0.7, 1, 1.5, 2, 2.75, 4]


fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize= (10, 10), layout="tight")

ax.view_init(azim=-40)
ax.dist = 12
for M in Mvals:
    z = fprime(svals, M, Z)
    z = np.where(z>=0, z, np.nan)
    ax.plot(svals, np.full(100, M), z, "r")

x = np.linspace(0, 4, 100)
y = np.linspace(0, 4, 100)
X, Y = np.meshgrid(x, y)
f = fprime(X, Y, Z)
f = np.where(f>0, f, 0)

ax.plot_wireframe(X, Y, f, alpha=0.9, linewidth=0.5)
ax.set_xlabel("s (Å⁻¹)", fontsize=12, labelpad=8)
ax.set_ylabel("B (Å²)", fontsize=12, labelpad=8)
ax.set_zlabel("f' (Å)", fontsize=12, labelpad=18)
ax.tick_params(axis='z', which='major', pad=10)
# %%
Bvals = np.array([0.01, 0.05, 0.1, 0.15, 0.2])
svals = np.linspace(0, 6, 100)
fig, ax = plt.subplots(figsize= (10, 10), layout="tight")
ax.set_xlabel("s (Å⁻¹)", fontsize=12)
ax.set_ylabel("f' (Å)", fontsize=12)
for B in Bvals:
    ydata = fprime(svals, B, Z)
    ax.plot(svals, ydata, label="B =" + str(B))
plt.legend()

# %%
