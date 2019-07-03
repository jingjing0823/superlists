QUnit.test( "hello test", function( assert ) {
  assert.ok( 1 == "1", "Passed!" );
});
  	QUnit.test("smoke test",function(assert){
  		assert.equal($(".has-error").is(':visible'),true);
  		$(".has-error").hide();
  		assert.equal($(".has-error").is(':visible'),false)
  		});